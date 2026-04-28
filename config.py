import cv2

# --- Параметры системы ---
MAX_OBJECTS = 5
MODEL_NAME = "best.pt"      # Путь к твоей модели с Roboflow
CONF_THRESHOLD = 0.5

# --- Визуал (BGR) ---
COLOR_BOX = (0, 255, 0)      # Рамка: Зеленый
COLOR_CENTER = (0, 255, 0)   # Центр: Зеленый
COLOR_TEXT = (255, 255, 255) # Текст: Белый
COLOR_TYPE_TEXT = (0, 165, 255) # Тип: Оранжевый
COLOR_ALERT = (0, 0, 255)    # ALERT: Красный
FONT = cv2.FONT_HERSHEY_SIMPLEX
THICKNESS = 2

# --- Логирование и Аудио ---
CONSOLE_UPDATE_RATE = 10     # Частота обновления консоли
ALERT_SOUND = "alert.wav"    # Звук в папке проекта
ALERT_DELAY = 0.25           # Задержка перед сиреной (сек)