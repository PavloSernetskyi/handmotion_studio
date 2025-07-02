import cv2

class VirtualObject:
    def __init__(self, x, y, width, height, color=(255, 0, 0), type="generic", image=None):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        self.type = type
        self.image = cv2.resize(image, (self.w, self.h)) if image is not None else None
        self.is_selected = False
        self.drinking = False

    def draw(self, frame):
        if self.image is not None:
            h, w = self.image.shape[:2]
            x1, y1 = self.x, self.y
            x2, y2 = x1 + w, y1 + h

            # Clip to frame dimensions
            x1_clip, y1_clip = max(0, x1), max(0, y1)
            x2_clip, y2_clip = min(frame.shape[1], x2), min(frame.shape[0], y2)

            if x2_clip <= x1_clip or y2_clip <= y1_clip:
                return  # Don't draw if outside the screen

            # Adjust image slice to match clipped area
            img_x1 = x1_clip - x1
            img_y1 = y1_clip - y1
            img_x2 = img_x1 + (x2_clip - x1_clip)
            img_y2 = img_y1 + (y2_clip - y1_clip)

            image_roi = self.image[img_y1:img_y2, img_x1:img_x2]

            if image_roi.shape[2] == 4:
                overlay = image_roi[:, :, :3]
                alpha = image_roi[:, :, 3] / 255.0
                for c in range(3):
                    frame[y1_clip:y2_clip, x1_clip:x2_clip, c] = (
                            frame[y1_clip:y2_clip, x1_clip:x2_clip, c] * (1 - alpha) +
                            overlay[:, :, c] * alpha
                    ).astype("uint8")
            else:
                frame[y1_clip:y2_clip, x1_clip:x2_clip] = image_roi

        else:
            color = (0, 255, 0) if self.is_selected else self.color
            cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), color, -1)

        # Label
        cv2.putText(frame, self.type, (self.x + 5, self.y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Drinking status
        if self.type == "beer" and self.drinking:
            cv2.putText(frame, "🍺 Opening beer and drinking...", (self.x, self.y + self.h + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    def contains(self, point):
        px, py = point
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def move_to(self, px, py):
        self.x = px - self.w // 2
        self.y = py - self.h // 2