import cv2
from config import (
    COLOR_BOX, COLOR_CENTER, COLOR_TEXT, COLOR_TYPE_TEXT,
    FONT, THICKNESS
)

class Visualizer:
    def draw(self, frame, objects):
        for obj in objects:
            x1, y1, x2, y2 = obj['bbox']
            cx, cy = obj['center']
            obj_id = obj['id']
            obj_name = obj['name']

            # 1. Рамка
            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_BOX, THICKNESS)

            # 2. Тип объекта
            type_label = obj_name.upper()
            (tw, th), _ = cv2.getTextSize(type_label, FONT, 0.5, 1)
            cv2.rectangle(frame, (x1, y1 - 20), (x1 + tw, y1), COLOR_TYPE_TEXT, -1)
            cv2.putText(frame, type_label, (x1, y1 - 5), FONT, 0.5, (0,0,0), 1)

            # 3. Номер объекта
            id_label = f"ID: {obj_id}"
            (iw, ih), _ = cv2.getTextSize(id_label, FONT, 0.5, 1)
            bg_y = y1 - 40 if y1 - 40 > 0 else y2 + 20
            cv2.rectangle(frame, (x1, bg_y), (x1 + iw, bg_y + ih), (0, 0, 0), -1)
            cv2.putText(frame, id_label, (x1, bg_y + ih - 2), FONT, 0.5, COLOR_TEXT, 1)

            # 4. Координаты
            coords = f"X:{cx} Y:{cy}"
            cv2.putText(frame, coords, (x1, y2 + 15), FONT, 0.5, COLOR_TEXT, 1)

            # 5. Центр
            cv2.circle(frame, (cx, cy), 5, COLOR_CENTER, -1)

        cv2.putText(frame, f"Active: {len(objects)}", (10, 30), FONT, 0.7, COLOR_TEXT, 2)
        return frame