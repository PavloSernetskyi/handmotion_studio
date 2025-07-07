import cv2
from objects import VirtualObject

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

def ball_hits_paddle(ball, paddle):
    return (
        paddle.x < ball.x < paddle.x + paddle.w and
        paddle.y < ball.y < paddle.y + paddle.h
    )

def run_pingpong(frame, landmarks, gestures, game_state):
    min_x, max_x = 100, 350
    min_y, max_y = 100, 460

    height, width, _ = frame.shape
    x1 = width - 220
    y1 = 20
    x2 = width - 20
    y2 = 70

    # Exit button
    cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 100), -1)
    cv2.putText(frame, "Back to Menu", (x1 + 10, y2 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    if landmarks and len(landmarks[0]) >= 9:
        index_tip = landmarks[0][8]
        x, y = index_tip
        if x1 < x < x2 and y1 < y < y2 and gestures[0] == "pinch":
            return "menu"  # Return control to menu

        cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)
        if game_state["paddle"].contains(index_tip):
            if gestures[0] == "grab":
                game_state["dragging_obj"] = game_state["paddle"]
                game_state["paddle"].is_selected = True
            elif gestures[0] == "open":
                game_state["dragging_obj"] = None
                game_state["paddle"].is_selected = False
        if game_state["dragging_obj"]:
            game_state["dragging_obj"].move_to(*index_tip)

    game_state["ball"].move()
    if game_state["ball"].x <= min_x or game_state["ball"].x >= max_x:
        game_state["ball"].vx *= -1
    if ball_hits_paddle(game_state["ball"], game_state["paddle"]):
        game_state["ball"].vy = -abs(game_state["ball"].vy)
    if ball_hits_paddle(game_state["ball"], game_state["ai_paddle"]):
        game_state["ball"].vy = abs(game_state["ball"].vy)
    if game_state["ball"].y > max_y:
        game_state["ai_score"] += 1
        game_state["ball"] = PingPongBall(340, 280, vx=-5, vy=-5)
    elif game_state["ball"].y < min_y:
        game_state["player_score"] += 1
        game_state["ball"] = PingPongBall(340, 280, vx=5, vy=5)

    game_state["ai_paddle"].x = max(min_x, min(game_state["ball"].x - game_state["ai_paddle"].w // 2, max_x - game_state["ai_paddle"].w))

    cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
    game_state["paddle"].draw(frame)
    game_state["ai_paddle"].draw(frame)
    game_state["ball"].draw(frame)
    cv2.putText(frame, f"You: {game_state['player_score']}   AI: {game_state['ai_score']}",
                (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    return "pingpong"
