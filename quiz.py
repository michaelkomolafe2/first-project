import sys
import select
from hardware import HARDWARE

# INPUT & ANSWER HELPERS

def get_safe_input(prompt, timeout=None):
    # Gets keyboard input. On Raspberry Pi hardware, enforces a timeout
    # using select. On PC, falls back to standard blocking input.
    # Returns None if the timeout expires with no input.
    if timeout and HARDWARE:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            print("\nTIME'S UP!")
            return None
        return sys.stdin.readline().strip().lower()
    else:
        return input(prompt).strip().lower()


def answer_check(user, correct):
    # Returns True if the correct answer string is found anywhere
    # in the user's answer. Case-insensitive.
    if user is None:
        return False
    return correct.lower() in user.lower()
