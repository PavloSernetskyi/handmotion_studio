import math

class GestureRecognizer:
    def __init__(self):
        pass

    def _distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.hypot(x2 - x1, y2 - y1)

    def recognize(self, landmarks_list):
        gestures = []

        for hand in landmarks_list:
            if not hand or len(hand) < 21:
                gestures.append(None)
                continue

            # Key landmarks
            thumb_tip = hand[4]
            index_tip = hand[8]
            middle_tip = hand[12]
            ring_tip = hand[16]
            pinky_tip = hand[20]

            index_base = hand[5]
            middle_base = hand[9]
            ring_base = hand[13]
            pinky_base = hand[17]

            def is_curled(tip, base):
                return self._distance(tip, base) < 80  # Loosened threshold

            # Count curled fingers (excluding thumb)
            curled_fingers = sum([
                is_curled(index_tip, index_base),
                is_curled(middle_tip, middle_base),
                is_curled(ring_tip, ring_base),
                is_curled(pinky_tip, pinky_base)
            ])

            # print(f"Curled fingers: {curled_fingers}")

            # ✊ Grab
            if curled_fingers >= 2:
                gestures.append("grab")

            # 🤏 Pinch
            elif self._distance(thumb_tip, index_tip) < 40 and curled_fingers < 2:
                gestures.append("pinch")

            # ✋ Open
            elif curled_fingers == 0:
                gestures.append("open")

            # Fallback
            else:
                gestures.append("grab" if curled_fingers >= 2 else "neutral")

        return gestures
