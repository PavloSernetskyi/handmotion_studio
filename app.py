from objects import VirtualObject
import cv2
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()

    # beer_img = cv2.imread("assets/beer_can.png", cv2.IMREAD_UNCHANGED)
    beer_img_original = cv2.imread("assets/beer_can.png", cv2.IMREAD_UNCHANGED)
    basketball_img_original = cv2.imread("assets/basketball.png", cv2.IMREAD_UNCHANGED)
    cube_img_original = cv2.imread("assets/cube.png", cv2.IMREAD_UNCHANGED)

    objects = [
        VirtualObject(100, 150, 200, 250, type="beer", image=beer_img_original), # Beer
        VirtualObject(300, 150, 150, 150, type="basketball", image=basketball_img_original),  # Basketball
        VirtualObject(200, 350, 100, 100, type="cube", image=cube_img_original)         # Cube
    ]
    dragging_obj = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #This makes the virtual cursor and object interactions match your real hand movement
        frame = cv2.flip(frame, 1)  # ← Flip horizontally to fix mirroring

        frame, landmarks = tracker.process(frame)
        gestures = recognizer.recognize(landmarks)

        # Track index finger of first hand (for interaction/dragging)
        if landmarks and len(landmarks[0]) >= 9:
            index_tip = landmarks[0][8]
            cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)  # Yellow cursor

            # Object interaction
            for obj in objects:
                if obj.contains(index_tip):
                    if gestures[0] == "grab":
                        dragging_obj = obj
                        obj.is_selected = True
                    elif gestures[0] == "open":
                        if dragging_obj == obj:
                            dragging_obj = None
                        obj.is_selected = False

                # 🍺 Trigger drinking if hand 0 grabs and hand 1 pinches
                if obj.type == "beer" and obj.contains(index_tip):
                    if len(gestures) >= 2:
                        if gestures[0] == "grab" and gestures[1] == "pinch":
                            obj.drinking = True
                        elif gestures[0] == "open" or gestures[1] == "open":
                            obj.drinking = False

            # Move selected object with index finger tip
            if dragging_obj:
                dragging_obj.move_to(*index_tip)

        # Draw all virtual objects
        for obj in objects:
            obj.draw(frame)

        # Display current gesture info
        if gestures:
            for i, g in enumerate(gestures):
                if g:
                    cv2.putText(frame, f"Hand {i+1}: {g}", (10, 30 + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("HandMotion Studio", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
