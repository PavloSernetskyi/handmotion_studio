import cv2

class VirtualObject:
    def __init__(self, x, y, width, height, color=(255, 0, 0), type="generic"):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        self.is_selected = False
        self.type = type  # e.g., 'beer', 'basketball', 'cube'

    def draw(self, frame):
        color = (0, 255, 0) if self.is_selected else self.color
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), color, -1)

    def contains(self, point):
        px, py = point
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def move_to(self, px, py):
        self.x = px - self.w // 2
        self.y = py - self.h // 2
