import time
import random

try:
    from gpiozero import LED, Button
    HARDWARE = True
except ImportError:
    HARDWARE = False

    class LED:
        def __init__(self, pin):
            self.pin = pin

        def on(self):
            print(f"[LED {self.pin} ON]")

        def off(self):
            print(f"[LED {self.pin} OFF]")

        def blink(self, on_time=1, off_time=1, **kwargs):
            print(f"[LED {self.pin} BLINK on={on_time}s off={off_time}s]")

    class Button:
        def __init__(self, pin):
            self.pin = pin
            self.when_pressed = None

        def press(self):
            if callable(self.when_pressed):
                self.when_pressed()

from config import LED_PINS, BUTTON_P1_PIN, BUTTON_P2_PIN

# ==========================================
# HARDWARE SETUP
# ==========================================
life_leds = [LED(pin) for pin in LED_PINS]
btn_p1 = Button(BUTTON_P1_PIN)
btn_p2 = Button(BUTTON_P2_PIN)

# Named references for clarity
led_p1    = life_leds[0]  # Player 1 indicator — leftmost LED
led_timer = life_leds[1]  # Shared timer indicator — middle LED
led_p2    = life_leds[2]  # Player 2 indicator — rightmost LED


# ==========================================
# LED HELPERS
# ==========================================
def set_all_leds(state):
    """Turns all LEDs 'on' or 'off'."""
    for led in life_leds:
        if state == 'on':
            led.on()
        else:
            led.off()


def set_timer_led(fast=False):
    """
    Starts the timer LED blinking.
    fast=False -> steady heartbeat-like effect (waiting for buzz)
    fast=True  -> frantic blink, rushing type of effect (player is answering)
    """
    if fast:
        led_timer.blink(on_time=0.2, off_time=0.2)
    else:
        led_timer.blink(on_time=0.5, off_time=0.5)


# ==========================================
# BUTTON HELPERS
# ==========================================
def wait_for_buzz(timeout, allowed_players=(1, 2)):
    """
    Waits for a hardware button press and returns the winning player number.
    Returns None if the timeout expires with no buzz.
    """
    if not HARDWARE:
        time.sleep(random.uniform(0.5, 2))
        return random.choice(allowed_players)

    winner = [None]

    def p1_pressed():
        if winner[0] is None and 1 in allowed_players:
            winner[0] = 1

    def p2_pressed():
        if winner[0] is None and 2 in allowed_players:
            winner[0] = 2

    btn_p1.when_pressed = p1_pressed
    btn_p2.when_pressed = p2_pressed

    start_time = time.time()
    while winner[0] is None and (time.time() - start_time) < timeout:
        time.sleep(0.01)

    btn_p1.when_pressed = None
    btn_p2.when_pressed = None

    return winner[0]
