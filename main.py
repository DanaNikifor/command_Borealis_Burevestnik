# main.py
import cv2
import time
import pygame
from collections import defaultdict, deque
from config import CONSOLE_UPDATE_RATE, ALERT_SOUND, ALERT_DELAY, COLOR_ALERT, FONT, THICKNESS, TRAJECTORY_MAX_LEN
from detector import Detector
from visualizer import Visualizer
from logger import ConsoleLogger

def main():
    cap = cv2.VideoCapture(1)
    detector = Detector()
    visualizer = Visualizer()
    logger = ConsoleLogger(CONSOLE_UPDATE_RATE)

    pygame.mixer.init()
    alert_sound = None
    try:
        alert_sound = pygame.mixer.Sound(ALERT_SOUND)
    except Exception as e:
        print(f"[!] Внимание: звук '{ALERT_SOUND}' не найден. ({e})")

    alert_active = False
    alert_acknowledged = False
    detection_start = None

    trajectories = defaultdict(lambda: deque(maxlen=TRAJECTORY_MAX_LEN))

    if not cap.isOpened():
        print("[!] Ошибка: Камера не найдена.")
        return

    print("[*] Запуск системы... 'q' - выход, 'ESC' - отключить сирену.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        objects = detector.get_objects(frame)
        
        # Обновляем траектории
        current_ids = set()
        for obj in objects:
            current_ids.add(obj['id'])
            trajectories[obj['id']].append(obj['center'])

        # СРАЗУ удаляем траектории потерянных объектов
        for lost_id in list(trajectories.keys()):
            if lost_id not in current_ids:
                del trajectories[lost_id]

        frame = visualizer.draw(frame, objects, trajectories)
        logger.log(objects)

        current_time = time.time()

        if len(objects) > 0:
            if detection_start is None:
                detection_start = current_time
                alert_acknowledged = False

            if not alert_active and not alert_acknowledged and (current_time - detection_start >= ALERT_DELAY):
                alert_active = True
                if alert_sound:
                    alert_sound.play(loops=-1)
                print("[!] ВНИМАНИЕ: Обнаружена цель! Оператор, примите решение.")
        else:
            detection_start = None
            if alert_active:
                alert_active = False
                if alert_sound:
                    alert_sound.stop()

        if alert_active:
            cv2.putText(frame, "🚨 ALERT ACTIVE", (10, 65), FONT, 0.8, COLOR_ALERT, THICKNESS)
        elif alert_acknowledged and len(objects) > 0:
            cv2.putText(frame, "🔇 ALERT ACKNOWLEDGED", (10, 65), FONT, 0.8, (200, 200, 200), THICKNESS)

        cv2.imshow("Burvestnik System", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            alert_acknowledged = True
            if alert_active:
                alert_active = False
                if alert_sound:
                    alert_sound.stop()
                print("[i] Оповещение отключено оператором. Ответственность принята.")
        elif key == ord('q'):
            break

    cap.release()
    if alert_sound:
        alert_sound.stop()
    pygame.mixer.quit()
    cv2.destroyAllWindows()
    print("[*] Система остановлена.")

if __name__ == "__main__":
    main()