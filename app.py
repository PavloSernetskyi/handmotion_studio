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
    return (
        paddle.x < ball.x < paddle.x + paddle.w and
        paddle.y < ball.y < paddle.y + paddle.h
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

def run_handmotion_studio():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()

    cv2.namedWindow("HandMotion Studio", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("HandMotion Studio", 1280, 720)

    mode = "menu"
    dragging_obj = None
    player_score = 0
    ai_score = 0

    min_x, max_x = 100, 350
    min_y, max_y = 100, 460

    beer_img = cv2.imread("assets/beer_can.png", cv2.IMREAD_UNCHANGED)
    basketball_img = cv2.imread("assets/basketball.png", cv2.IMREAD_UNCHANGED)
    cube_img = cv2.imread("assets/cube.png", cv2.IMREAD_UNCHANGED)
    paddle_img = cv2.imread("assets/paddle.png", cv2.IMREAD_UNCHANGED)

    paddle = VirtualObject(340, 400, 100, 150, type="paddle", image=paddle_img)
    ai_paddle = VirtualObject(340, min_y, 100, 120, type="ai", image=paddle_img)
    ball = PingPongBall(340, 280)

    playground_objects = [
        VirtualObject(100, 150, 200, 250, type="beer", image=beer_img),
        VirtualObject(300, 150, 150, 150, type="basketball", image=basketball_img),
        VirtualObject(200, 350, 100, 100, type="cube", image=cube_img)
    ]

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame, landmarks = tracker.process(frame)
        gestures = recognizer.recognize(landmarks)

        height, width, _ = frame.shape
        button_width = 200
        button_height = 50
        x1 = width - button_width - 20
        y1 = height - button_height - 20
        x2 = width - 20
        y2 = height - 20

        if mode != "menu":
            cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 100), -1)
            cv2.putText(frame, "Back to Menu", (x1 + 10, y2 - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if mode == "menu":
            cv2.rectangle(frame, (20, 20), (200, 80), (0, 200, 0), -1)
            cv2.putText(frame, "Ping Pong", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (220, 20), (420, 80), (0, 0, 200), -1)
            cv2.putText(frame, "Playground", (230, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if landmarks and len(landmarks[0]) >= 9:
                index_tip = landmarks[0][8]
                cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)
                x, y = index_tip
                if 20 < x < 200 and 20 < y < 80 and gestures[0] == "pinch":
                    mode = "pingpong"
                elif 220 < x < 420 and 20 < y < 80 and gestures[0] == "pinch":
                    mode = "playground"

        elif mode == "pingpong":
            if landmarks and len(landmarks[0]) >= 9:
                index_tip = landmarks[0][8]
                x, y = index_tip
                if x1 < x < x2 and y1 < y < y2 and gestures[0] == "pinch":
                    mode = "menu"
                    continue

            ball.move()
            if ball.x <= min_x or ball.x >= max_x:
                ball.vx *= -1
            if ball_hits_paddle(ball, paddle):
                ball.vy = -abs(ball.vy)
            if ball_hits_paddle(ball, ai_paddle):
                ball.vy = abs(ball.vy)
            if ball.y > max_y:
                ai_score += 1
                ball = PingPongBall(340, 280, vx=-5, vy=-5)
            elif ball.y < min_y:
                player_score += 1
                ball = PingPongBall(340, 280, vx=5, vy=5)

            ai_paddle.x = max(min_x, min(ball.x - ai_paddle.w // 2, max_x - ai_paddle.w))

            if landmarks and len(landmarks[0]) >= 9:
                index_tip = landmarks[0][8]
                cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)
                if paddle.contains(index_tip):
                    if gestures[0] == "grab":
                        dragging_obj = paddle
                        paddle.is_selected = True
                    elif gestures[0] == "open":
                        dragging_obj = None
                        paddle.is_selected = False
                if dragging_obj:
                    dragging_obj.move_to(*index_tip)

            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
            paddle.draw(frame)
            ai_paddle.draw(frame)
            ball.draw(frame)
            cv2.putText(frame, f"You: {player_score}   AI: {ai_score}", (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        elif mode == "playground":
            if landmarks and len(landmarks[0]) >= 9:
                index_tip = landmarks[0][8]
                x, y = index_tip
                if x1 < x < x2 and y1 < y < y2 and gestures[0] == "pinch":
                    mode = "menu"
                    continue
                cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)

                for obj in playground_objects:
                    if obj.contains(index_tip):
                        if gestures[0] == "grab":
                            dragging_obj = obj
                            obj.is_selected = True
                        elif gestures[0] == "open":
                            if dragging_obj == obj:
                                dragging_obj = None
                            obj.is_selected = False

                    if obj.type == "beer":
                        if len(landmarks) >= 2 and len(gestures) >= 2 and not is_duplicate_hand(landmarks[0], landmarks[1]):
                            if dragging_obj == obj and gestures[0] == "grab" and gestures[1] == "pinch":
                                obj.drinking = True
                            elif gestures[0] == "open" or gestures[1] == "open":
                                obj.drinking = False

                if dragging_obj:
                    dragging_obj.move_to(*index_tip)

            for obj in playground_objects:
                obj.draw(frame)

        if gestures:
            for i, g in enumerate(gestures):
                if g:
                    cv2.putText(frame, f"Hand {i+1}: {g}", (10, 90 + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("HandMotion Studio", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_handmotion_studio()
