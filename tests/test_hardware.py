import unittest
from unittest.mock import patch
import io

from hardware import (
    HARDWARE,
    led_p1, led_p2, led_timer,
    set_all_leds,
    set_timer_led,
    LED_PINS
)


class TestDummyLED(unittest.TestCase):
    """
    Tests for the dummy LED class used in PC simulation mode.
    Verifies that LED state changes print the correct terminal output.
    """

    def test_led_on_prints_correct_pin(self):
        """led_p1.on() should print the correct GPIO pin number."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            led_p1.on()
            self.assertIn(str(led_p1.pin), mock_out.getvalue())
            self.assertIn("ON", mock_out.getvalue())

    def test_led_off_prints_correct_pin(self):
        """led_p1.off() should print the correct GPIO pin number."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            led_p1.off()
            self.assertIn(str(led_p1.pin), mock_out.getvalue())
            self.assertIn("OFF", mock_out.getvalue())

    def test_led_blink_prints_timing(self):
        """led_timer.blink() should print on_time and off_time values."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            led_timer.blink(on_time=0.5, off_time=0.5)
            output = mock_out.getvalue()
            self.assertIn("0.5", output)
            self.assertIn("BLINK", output)

    def test_all_leds_on(self):
        """set_all_leds('on') should trigger on() for every LED."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            set_all_leds('on')
            output = mock_out.getvalue()
            for pin in LED_PINS:
                self.assertIn(str(pin), output)
            self.assertIn("ON", output)

    def test_all_leds_off(self):
        """set_all_leds('off') should trigger off() for every LED."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            set_all_leds('off')
            output = mock_out.getvalue()
            self.assertIn("OFF", output)


class TestTimerLED(unittest.TestCase):
    """
    Tests for the set_timer_led() helper.
    Verifies the correct blink timing is used for each game state.
    """

    def test_slow_blink_when_waiting(self):
        """fast=False should produce a slow 0.5s heartbeat blink."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            set_timer_led(fast=False)
            self.assertIn("0.5", mock_out.getvalue())

    def test_fast_blink_when_answering(self):
        """fast=True should produce a fast 0.2s frantic blink."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            set_timer_led(fast=True)
            self.assertIn("0.2", mock_out.getvalue())


class TestLEDPinAssignment(unittest.TestCase):
    """
    Tests that named LED references point to the correct GPIO pins.
    This protects against accidental rewiring in config.py.
    """

    def test_led_p1_is_first_pin(self):
        """Player 1 LED should be on the first pin in LED_PINS."""
        self.assertEqual(led_p1.pin, LED_PINS[0])

    def test_led_timer_is_middle_pin(self):
        """Timer LED should be on the middle pin in LED_PINS."""
        self.assertEqual(led_timer.pin, LED_PINS[1])

    def test_led_p2_is_last_pin(self):
        """Player 2 LED should be on the last pin in LED_PINS."""
        self.assertEqual(led_p2.pin, LED_PINS[2])


if __name__ == "__main__":
    unittest.main()
