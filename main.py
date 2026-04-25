import sys

from config import QUIZ_DATA
from hardware import set_all_leds
from quiz import get_safe_input
from modes.single_player import play_single_player
from modes.two_player import play_two_player


# ==========================================
# MAIN MENU
# ==========================================
def main():
    print("=== Welcome to the Quiz! ===")
    mode = get_safe_input("Game Mode - A) Single Player  B) 2 Player\n> ").upper()

    if mode == "B":
        p1_name = get_safe_input("Enter Player 1's name: ").title()
        p2_name = get_safe_input("Enter Player 2's name: ").title()
    else:
        p1_name = get_safe_input("Enter your name: ").title()
        p2_name = None

    diff_choice = get_safe_input("Choose Difficulty - A) Easy  B) Medium  C) Hard\n> ").upper()
    selected_quiz = QUIZ_DATA.get(diff_choice)

    if not selected_quiz:
        print("Invalid difficulty selected. Exiting...")
        sys.exit()

    if mode == "B":
        play_two_player(selected_quiz, p1_name, p2_name)
    else:
        play_single_player(selected_quiz)


# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    try:
        while True:
            main()
            again = get_safe_input("\nDo you want to play again? (y/n): ")
            if again == "n":
                break
    except KeyboardInterrupt:
        print("\nUser left game.")
    finally:
        set_all_leds('off')
