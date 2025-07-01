# from objects import VirtualObject
# import cv2
# from hand_tracker import HandTracker
# from gesture_recognizer import GestureRecognizer
#
# def main():
#     cap = cv2.VideoCapture(0)
#     tracker = HandTracker()
#     recognizer = GestureRecognizer()
#
#     # Multiple virtual objects with different positions/colors
#     objects = [
#         VirtualObject(100, 150, 100, 100, (255, 0, 0), "beer"),  # Beer
#         VirtualObject(300, 150, 100, 100, (0, 255, 0), "basketball"),
#         VirtualObject(200, 350, 100, 100, (0, 0, 255), "cube")
#     ]
#     dragging_obj = None
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame, landmarks = tracker.process(frame)
#
#         gesture = recognizer.recognize(landmarks)
#
#         # Only run if we have landmarks
#         if landmarks and len(landmarks[0]) >= 9:
#             index_tip = landmarks[0][8]
#             cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)
#
#             # Interaction: Check all objects
#             for obj in objects:
#                 if obj.contains(index_tip):
#                     if gesture == "grab":
#                         dragging_obj = obj
#                         obj.is_selected = True
#                     elif gesture == "open":
#                         if dragging_obj == obj:
#                             dragging_obj = None
#                         obj.is_selected = False
#
#                 # simulate beer drinking
#                 if obj.type == "beer" and obj.contains(index_tip):
#                     if gesture == "grab":
#                         obj.drinking = True
#                     elif gesture == "open":
#                         obj.drinking = False
#
#             # Move selected object
#             if dragging_obj:
#                 dragging_obj.move_to(*index_tip)
#
#         # Draw all objects
#         for obj in objects:
#             obj.draw(frame)
#
#         if gesture:
#             cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#         # Draw virtual cursor if hand is detected
#         if landmarks and len(landmarks[0]) >= 9:  # make sure index tip exists
#             index_tip = landmarks[0][8]  # landmark 8 is index finger tip
#             cv2.circle(frame, index_tip, 12, (0, 255, 255), -1)  # Yellow cursor
#
#         cv2.imshow("HandMotion Studio", frame)
#
#         if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     main()


from objects import VirtualObject
import cv2
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()

    objects = [
        VirtualObject(100, 150, 100, 100, (255, 0, 0), "beer"),        # Beer
        VirtualObject(300, 150, 100, 100, (0, 255, 0), "basketball"),  # Basketball
        VirtualObject(200, 350, 100, 100, (0, 0, 255), "cube")         # Cube
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
