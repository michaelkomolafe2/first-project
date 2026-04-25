import random

from hardware import set_all_leds, life_leds
from quiz import get_safe_input, answer_check


# ==========================================
# SINGLE PLAYER GAME MODE
# ==========================================
def play_single_player(quiz):
    """Handles the 1-Player game loop."""
    set_all_leds('on')
    score = 0
    lives = 3
    time_limit = quiz["time_limit"]

    questions = quiz["questions"].copy()
    random.shuffle(questions)

    print(f"\n--- {quiz['difficulty']} Mode: You have {time_limit}s per question! ---")

    for item in questions:
        if lives <= 0:
            print("\nGame Over! You ran out of lives.")
            break

        print(f"\nQuestion: {item['q']}")
        guess = get_safe_input("Your answer: ", timeout=time_limit)

        if answer_check(guess, item['a']):
            print("Correct!")
            score += 1
        else:
            lives -= 1
            if guess is None:
                print(f"Time's up! The answer was: {item['a'].title()}")
            else:
                print(f"Wrong! The answer was: {item['a'].title()}")
            print(f"Lives remaining: {lives}")

            if lives > 0:
                life_leds[lives - 1].off()  # Turn off one LED per life lost

    print(f"\nQuiz finished! You scored {score} out of {len(quiz['questions'])}.")
