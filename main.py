import cv2
import time
import pygame
from config import CONSOLE_UPDATE_RATE, ALERT_SOUND, ALERT_DELAY, COLOR_ALERT, FONT, THICKNESS
from detector import Detector
from visualizer import Visualizer
from logger import ConsoleLogger

def main():
    cap = cv2.VideoCapture(1)
    detector = Detector()
    visualizer = Visualizer()
    logger = ConsoleLogger(CONSOLE_UPDATE_RATE)

    # --- Инициализация звука ---
    pygame.mixer.init()
    alert_sound = None
    try:
        alert_sound = pygame.mixer.Sound(ALERT_SOUND)
    except Exception as e:
        print(f"[!] Внимание: звук '{ALERT_SOUND}' не найден или не поддерживается. ({e})")

    # --- Состояние системы ---
    alert_active = False
    alert_acknowledged = False
    detection_start = None

    if not cap.isOpened():
        print("[!] Ошибка: Камера не найдена.")
        return

    print("[*] Запуск системы... 'q' - выход, 'ESC' - отключить сирену.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        objects = detector.get_objects(frame)
        frame = visualizer.draw(frame, objects)
        logger.log(objects)

        current_time = time.time()

        # --- Логика оповещения ---
        if len(objects) > 0:
            if detection_start is None:
                detection_start = current_time
                alert_acknowledged = False  # Сброс при новом обнаружении

            # Если цель держится > 0.25 сек и сирена не активна/не отключена
            if not alert_active and not alert_acknowledged and (current_time - detection_start >= ALERT_DELAY):
                alert_active = True
                if alert_sound:
                    alert_sound.play(loops=-1)  # -1 = бесконечный цикл
                print("[!] ВНИМАНИЕ: Обнаружена цель! Оператор, примите решение.")
        else:
            detection_start = None
            if alert_active:
                alert_active = False
                if alert_sound:
                    alert_sound.stop()

        # Визуальный индикатор сирены на кадре
        if alert_active:
            cv2.putText(frame, "🚨 ALERT ACTIVE", (10, 65), FONT, 0.8, COLOR_ALERT, THICKNESS)
        elif alert_acknowledged and len(objects) > 0:
            cv2.putText(frame, "🔇 ALERT ACKNOWLEDGED", (10, 65), FONT, 0.8, (200, 200, 200), THICKNESS)

        cv2.imshow("Burvestnik System", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            alert_acknowledged = True
            if alert_active:
                alert_active = False
                if alert_sound:
                    alert_sound.stop()
                print("[i] Оповещение отключено оператором. Ответственность принята.")
        elif key == ord('q'):
            break

    # Очистка
    cap.release()
    if alert_sound:
        alert_sound.stop()
    pygame.mixer.quit()
    cv2.destroyAllWindows()
    print("[*] Система остановлена.")

if __name__ == "__main__":
    main()