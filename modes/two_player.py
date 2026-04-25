import random

from hardware import set_all_leds, set_timer_led, led_p1, led_p2, led_timer, wait_for_buzz
from quiz import get_safe_input, answer_check
from config import STEAL_TIME


# ==========================================
# TWO PLAYER GAME MODE
# ==========================================
def play_two_player(quiz, p1_name, p2_name):
    """Handles the 2-Player competitive game loop."""
    set_all_leds('off')
    scores = {1: 0, 2: 0}
    names = {1: p1_name, 2: p2_name}
    leds = {1: led_p1, 2: led_p2}
    time_limit = quiz["time_limit"]

    questions = quiz["questions"].copy()
    random.shuffle(questions)

    print(f"\n--- 2 Player Mode: {p1_name} vs {p2_name}! ---")

    for item in questions:
        print(f"\nQuestion: {item['q']}\n> Buzz in! ({time_limit}s)")

        # Steady heartbeat blink while waiting for a buzz
        set_timer_led(fast=False)
        first_buzzer = wait_for_buzz(time_limit)
        led_timer.off()

        if not first_buzzer:
            print(f"Nobody buzzed in! The answer was: {item['a'].title()}")
            continue

        other_player = 3 - first_buzzer

        # First player's attempt
        leds[first_buzzer].on()
        set_timer_led(fast=True)
        guess = get_safe_input(f"{names[first_buzzer]}, your answer: ", timeout=time_limit)
        led_timer.off()
        leds[first_buzzer].off()

        if answer_check(guess, item['a']):
            print(f"Correct! {names[first_buzzer]} scores a point!")
            scores[first_buzzer] += 1
            continue

        # Steal attempt
        if guess is not None:
            print("Wrong!")

        print(f"{names[other_player]}, press your button to steal! ({STEAL_TIME}s)")

        # Steady blink again for the steal window
        set_timer_led(fast=False)
        steal_buzzer = wait_for_buzz(STEAL_TIME, allowed_players=(other_player,))
        led_timer.off()

        if steal_buzzer:
            leds[other_player].on()
            set_timer_led(fast=True)
            steal_guess = get_safe_input(
                f"{names[other_player]}, your answer: ", timeout=time_limit
            )
            led_timer.off()
            leds[other_player].off()

            if answer_check(steal_guess, item['a']):
                print(f"Correct! {names[other_player]} steals the point!")
                scores[other_player] += 1
            else:
                if steal_guess is not None:
                    print("Wrong!")
                print(f"No points! The answer was: {item['a'].title()}")
        else:
            print(f"No steal attempt. The answer was: {item['a'].title()}")

    # Declare winner
    print("\n--- Final Scores ---")
    print(f"{p1_name}: {scores[1]} | {p2_name}: {scores[2]}")

    if scores[1] > scores[2]:
        print(f"{p1_name} wins!")
    elif scores[2] > scores[1]:
        print(f"{p2_name} wins!")
    else:
        print("It's a tie!")
