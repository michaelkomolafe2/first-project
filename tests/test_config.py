import unittest
from config import QUIZ_DATA, STEAL_TIME, LED_PINS, BUTTON_P1_PIN, BUTTON_P2_PIN


class TestQuizData(unittest.TestCase):
    """
    Tests for the structure and integrity of QUIZ_DATA loaded from questions.json.
    These tests ensure that any edits to questions.json don't silently break the game.
    """

    def test_all_difficulties_present(self):
        """QUIZ_DATA must contain all three difficulty keys."""
        self.assertIn("A", QUIZ_DATA)
        self.assertIn("B", QUIZ_DATA)
        self.assertIn("C", QUIZ_DATA)

    def test_each_difficulty_has_required_fields(self):
        """Every difficulty must have a questions list, difficulty label, and time limit."""
        for key, quiz in QUIZ_DATA.items():
            self.assertIn("questions", quiz, f"Difficulty {key} missing 'questions'")
            self.assertIn("difficulty", quiz, f"Difficulty {key} missing 'difficulty'")
            self.assertIn("time_limit", quiz, f"Difficulty {key} missing 'time_limit'")

    def test_time_limits_are_positive(self):
        """Time limits must be positive integers — a zero or negative value
        would cause the timer to expire instantly."""
        for key, quiz in QUIZ_DATA.items():
            self.assertGreater(
                quiz["time_limit"], 0,
                f"Difficulty {key} has an invalid time_limit"
            )

    def test_each_question_has_q_and_a(self):
        """Every question must have both a 'q' (question) and 'a' (answer) key.
        A missing key would crash the game mid-round."""
        for key, quiz in QUIZ_DATA.items():
            for i, item in enumerate(quiz["questions"]):
                self.assertIn("q", item, f"Difficulty {key}, question {i} missing 'q'")
                self.assertIn("a", item, f"Difficulty {key}, question {i} missing 'a'")

    def test_no_empty_questions_or_answers(self):
        """Questions and answers must not be empty strings.
        An empty answer would cause every guess to pass incorrectly."""
        for key, quiz in QUIZ_DATA.items():
            for i, item in enumerate(quiz["questions"]):
                self.assertTrue(
                    item["q"].strip(),
                    f"Difficulty {key}, question {i} has an empty question"
                )
                self.assertTrue(
                    item["a"].strip(),
                    f"Difficulty {key}, question {i} has an empty answer"
                )

    def test_minimum_question_count(self):
        """Each difficulty should have at least 5 questions to make the game worthwhile."""
        for key, quiz in QUIZ_DATA.items():
            self.assertGreaterEqual(
                len(quiz["questions"]), 5,
                f"Difficulty {key} has fewer than 5 questions"
            )


class TestHardwareConfig(unittest.TestCase):
    """
    Tests for hardware constants defined in config.py.
    Ensures pin numbers and timing values are valid before the game runs.
    """

    def test_steal_time_is_positive(self):
        """STEAL_TIME must be a positive number — zero would give no steal window."""
        self.assertGreater(STEAL_TIME, 0)

    def test_correct_number_of_leds(self):
        """The game expects exactly 3 LEDs — one per player and one timer."""
        self.assertEqual(len(LED_PINS), 3)

    def test_no_duplicate_pins(self):
        """All GPIO pin numbers must be unique — duplicate pins would
        cause hardware conflicts on the Pi."""
        all_pins = LED_PINS + [BUTTON_P1_PIN, BUTTON_P2_PIN]
        self.assertEqual(len(all_pins), len(set(all_pins)))


if __name__ == "__main__":
    unittest.main()
