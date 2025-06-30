import cv2
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, landmarks = tracker.process(frame)

        gesture = recognizer.recognize(landmarks)
        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw virtual cursor if hand is detected
        if landmarks and len(landmarks[0]) >= 9:  # make sure index tip exists
            index_tip = landmarks[0][8]  # landmark 8 is index finger tip
            cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)  # Yellow cursor

        cv2.imshow("HandMotion Studio", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
