import cv2

# --- Параметры системы ---
MAX_OBJECTS = 5
MODEL_NAME = "best.pt"
CONF_THRESHOLD = 0.5

# --- Визуал (BGR) ---
COLOR_BOX = (0, 255, 0)
COLOR_CENTER = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_TYPE_TEXT = (0, 165, 255)
COLOR_ALERT = (0, 0, 255)
TRAJECTORY_COLOR = (255, 0, 255)  # Маджента
TRAJECTORY_THICKNESS = 2
TRAJECTORY_MAX_LEN = 40           # Длина хвоста траектории

FONT = cv2.FONT_HERSHEY_SIMPLEX
THICKNESS = 2

# --- Логирование и Аудио ---
CONSOLE_UPDATE_RATE = 10
ALERT_SOUND = "alert.wav"
ALERT_DELAY = 0.25