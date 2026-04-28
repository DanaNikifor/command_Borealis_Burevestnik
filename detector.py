from ultralytics import YOLO
from config import MODEL_NAME, CONF_THRESHOLD, MAX_OBJECTS

class Detector:
    def __init__(self):
        print(f"[*] Загрузка модели {MODEL_NAME}...")
        self.model = YOLO(MODEL_NAME)
        self.class_names = self.model.names
        print("[+] Модель готова.")

    def get_objects(self, frame):
        results = self.model.track(
            source=frame, 
            persist=True, 
            conf=CONF_THRESHOLD, 
            max_det=MAX_OBJECTS,
            verbose=False
        )

        objects = []
        if results[0].boxes.id is not None:
            boxes = results[0].boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                obj_id = int(box.id[0].tolist())
                class_id = int(box.cls[0].tolist())
                obj_name = self.class_names.get(class_id, "unknown")
                
                objects.append({
                    'id': obj_id,
                    'name': obj_name,
                    'bbox': (x1, y1, x2, y2),
                    'center': (cx, cy)
                })
        return objects