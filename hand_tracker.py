import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.6):
        self.max_num_hands = max_num_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        hand_landmarks = []

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
                single_hand = []
                for lm in handLms.landmark:
                    h, w, c = frame.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    single_hand.append((x, y))
                hand_landmarks.append(single_hand)

        return frame, hand_landmarks
