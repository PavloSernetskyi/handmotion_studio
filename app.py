import cv2
from hand_tracker import HandTracker

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, landmarks = tracker.process(frame)
        cv2.imshow("HandMotion Studio", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
