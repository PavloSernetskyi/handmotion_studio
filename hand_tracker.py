import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1):
        self.max_num_hands = max_num_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        hand_landmarks = []

        if result.multi_hand_landmarks:
            for hand_landmarks_set in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks_set, self.mp_hands.HAND_CONNECTIONS)

                hand = []
                h, w, _ = frame.shape
                for lm in hand_landmarks_set.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    hand.append((x, y))
                hand_landmarks.append(hand)

        return frame, hand_landmarks
