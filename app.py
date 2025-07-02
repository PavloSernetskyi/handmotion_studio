from objects import VirtualObject
import cv2
import math
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer

def distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def is_duplicate_hand(hand1, hand2):
    if not hand1 or not hand2 or len(hand1) != len(hand2):
        return False
    close_points = 0
    for i in range(len(hand1)):
        dx = hand1[i][0] - hand2[i][0]
        dy = hand1[i][1] - hand2[i][1]
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist < 10:
            close_points += 1
    return close_points > 0.95 * len(hand1)

def ball_hits_paddle(ball, paddle):
    bx, by = ball.x, ball.y
    return (
        paddle.x < bx < paddle.x + paddle.w and
        paddle.y < by < paddle.y + paddle.h
    )

class PingPongBall:
    def __init__(self, x, y, vx=5, vy=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 15

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), self.radius, (255, 255, 255), -1)

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()

    cv2.namedWindow("HandMotion Studio", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("HandMotion Studio", 1280, 720)

    # Updated table area
    min_x, max_x = 100, 350
    min_y, max_y = 100, 460

    # Load images
    beer_img_original = cv2.imread("assets/beer_can.png", cv2.IMREAD_UNCHANGED)
    basketball_img_original = cv2.imread("assets/basketball.png", cv2.IMREAD_UNCHANGED)
    cube_img_original = cv2.imread("assets/cube.png", cv2.IMREAD_UNCHANGED)
    paddle_img_original = cv2.imread("assets/paddle.png", cv2.IMREAD_UNCHANGED)

    # Create objects
    paddle = VirtualObject(340, 400, 100, 150, type="paddle", image=paddle_img_original)
    ai_paddle = VirtualObject(340, min_y, 100, 120, type="ai", image=paddle_img_original)
    ball = PingPongBall(340, 280, vx=5, vy=5)


    objects = [
        VirtualObject(100, 150, 200, 250, type="beer", image=beer_img_original), # Beer
        VirtualObject(300, 150, 150, 150, type="basketball", image=basketball_img_original),  # Basketball
        VirtualObject(200, 350, 100, 100, type="cube", image=cube_img_original),        # Cube
        paddle,
        ai_paddle
    ]

    dragging_obj = None
    player_score = 0
    ai_score = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #This makes the virtual cursor and object interactions match your real hand movement
        frame = cv2.flip(frame, 1)  # ← Flip horizontally to fix mirroring

        frame, landmarks = tracker.process(frame)
        gestures = recognizer.recognize(landmarks)
        # Track index finger of first hand (for interaction/dragging)
        ball.move()

        # Ball bouncing
        if ball.x <= min_x or ball.x >= max_x:
            ball.vx *= -1

        # Paddle collisions
        if ball_hits_paddle(ball, paddle):
            ball.vy = -abs(ball.vy)
        if ball_hits_paddle(ball, ai_paddle):
            ball.vy = abs(ball.vy)

        # Scoring logic
        if ball.y > max_y:
            ai_score += 1
            ball = PingPongBall(340, 280, vx=-5, vy=-5)
        elif ball.y < min_y:
            player_score += 1
            ball = PingPongBall(340, 280, vx=5, vy=5)

        # AI paddle movement
        ai_paddle.x = max(min_x, min(ball.x - ai_paddle.w // 2, max_x - ai_paddle.w))

        # Interaction with objects
        if landmarks and len(landmarks[0]) >= 9:
            index_tip = landmarks[0][8]
            cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)  # Yellow cursor

            for obj in objects:
                if obj.contains(index_tip):
                    if gestures[0] == "grab":
                        dragging_obj = obj
                        obj.is_selected = True
                    elif gestures[0] == "open":
                        if dragging_obj == obj:
                            dragging_obj = None
                        obj.is_selected = False

                if obj.type == "beer" and obj.contains(index_tip):
                    if len(landmarks) >= 2 and len(gestures) >= 2:
                        if not is_duplicate_hand(landmarks[0], landmarks[1]):
                            if dragging_obj == obj and gestures[0] == "grab" and gestures[1] == "pinch":
                                obj.drinking = True
                            elif gestures[0] == "open" or gestures[1] == "open":
                                obj.drinking = False
                        else:
                            obj.drinking = False
                    else:
                        obj.drinking = False

            if dragging_obj:
                dragging_obj.move_to(*index_tip)
        # Draw all virtual objects
        # Draw table
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

        # Draw all objects
        for obj in objects:
            obj.draw(frame)

        ball.draw(frame)

        cv2.putText(frame, f"You: {player_score}   AI: {ai_score}", (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        if gestures:
            for i, g in enumerate(gestures):
                if g:
                    cv2.putText(frame, f"Hand {i+1}: {g}", (10, 90 + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("HandMotion Studio", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
