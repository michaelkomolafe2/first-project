import json
import os

# HARDWARE PINS

BUTTON_P1_PIN = 5
BUTTON_P2_PIN = 13
LED_PINS = [6, 19, 11]

# TIMING

STEAL_TIME = 5

# QUIZ DATA

_QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")
with open(_QUESTIONS_PATH) as f:
    QUIZ_DATA = json.load(f)