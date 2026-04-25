import unittest
from quiz import answer_check


class TestAnswerCheck(unittest.TestCase):
    """
    Tests for the answer_check() function.
    answer_check(user, correct) returns True if the correct answer
    is found anywhere inside the user's answer, case-insensitively.
    """

    def test_exact_match(self):
        """A perfect answer should return True."""
        self.assertTrue(answer_check("cheetah", "cheetah"))

    def test_case_insensitive(self):
        """Answers should match regardless of capitalisation."""
        self.assertTrue(answer_check("Cheetah", "cheetah"))
        self.assertTrue(answer_check("CHEETAH", "cheetah"))

    def test_partial_match(self):
        """A user can include extra words and still be correct.
        e.g. 'The Nile River' should match the answer 'nile'."""
        self.assertTrue(answer_check("The Nile River", "nile"))
        self.assertTrue(answer_check("Leonardo Da Vinci", "leonardo da vinci"))

    def test_wrong_answer(self):
        """A completely wrong answer should return False."""
        self.assertFalse(answer_check("amazon", "nile"))

    def test_none_input(self):
        """None is passed when the timer expires with no input.
        This should return False, not raise an error."""
        self.assertFalse(answer_check(None, "cheetah"))

    def test_empty_string(self):
        """An empty string answer should return False."""
        self.assertFalse(answer_check("", "cheetah"))

    def test_partial_wrong_match(self):
        """A word that contains the answer as a substring should not
        incorrectly pass. e.g. 'mars' should not match 'ar'."""
        self.assertFalse(answer_check("mars", "earth"))


if __name__ == "__main__":
    unittest.main()
