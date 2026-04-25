# 🕹️ Raspberry Pi Terminal Quiz Game

A fast-paced, terminal-based trivia game designed for the Raspberry Pi with full physical button and LED integration. 
Whether you're a maker building a hardware quiz buzzer system or a developer testing locally on your PC, this project offers an extensible, plug-and-play trivia experience for 1 or 2 players.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start (PC Simulation Mode)](#-quick-start-pc-simulation-mode)
- [🍓 Hardware Setup (Raspberry Pi)](#-hardware-setup-raspberry-pi)
- [🎮 How to Play](#-how-to-play)
- [✏️ Customizing Questions](#️-customizing-questions)
- [🛠️ Project Structure](#️-project-structure)
- [🧪 Development & Testing Guide](#-development--testing-guide)

---

## ✨ Features

- 👤 **Single Player Mode:** Race against the clock with 3 lives (tracked by real physical LEDs).
- 👥 **2-Player Versus Mode:** True hardware buzz-in mechanics. Steal points from your opponent on wrong answers!
- 🎚️ **Adaptive Difficulty:** Choose between Easy (15s), Medium (10s), and Hard (10s) question sets.
- 💻 **Hardware Abstraction:** Runs flawlessly on a PC (with randomized terminal simulation) or on a Raspberry Pi with physical buttons and LEDs.

---

## 🚀 Quick Start (PC Simulation Mode)

You don't need a Raspberry Pi to play or develop. The game automatically detects your environment and falls back to a terminal simulation mode if hardware isn't present.

**Requirements:** Python 3.7+ (No third-party packages needed for PC)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/first-game.git

# 2. Navigate into the directory
cd first-game

# 3. Run the game!
python3 main.py
```

---

## 🍓 Hardware Setup (Raspberry Pi)

Ready to play with real buttons and lights? Here is how to wire up your Pi.

### Wiring

| Component              | GPIO Pin |
|------------------------|----------|
| Player 1 Button        | GPIO 5   |
| Player 2 Button        | GPIO 13  |
| LED 1 (P1 Indicator / Life 1) | GPIO 6   |
| LED 2 (Timer)          | GPIO 19  |
| LED 3 (P2 Indicator / Life 3) | GPIO 11  |

### Installation

Raspberry Pi OS includes `gpiozero` by default. If you are using a lite or custom OS, install it via pip:

```bash
pip3 install gpiozero
```

Run the game exactly the same way:

```bash
python3 main.py
```

---

## 🎮 How to Play

### Single Player
1. Choose a difficulty level.
2. Answer each question before the timer runs out.
3. A wrong answer or timeout costs one life (watch the LEDs turn off!).
4. The game ends when all 3 lives are lost or all questions are exhausted.

### Two Player
1. Get your fingers on the hardware buttons!
2. When a question appears, the first to physically buzz in gets to answer.
3. **Steal Window:** If a player answers incorrectly, a brief steal window opens for the opponent to buzz in and steal the point.
4. The player with the most points at the end wins.

---

## ✏️ Customizing Questions

Adding your own trivia is as easy as editing a JSON file — no Python knowledge required! Open `questions.json` and add your questions under the desired difficulty (`A` for Easy, `B` for Medium, `C` for Hard):

```json
{ "q": "What is the capital of France?", "a": "paris" }
```

> **Note:** Answers are matched case-insensitively and support partial matches. For example, setting the answer to `"nile"` will correctly accept user input like `"The Nile River"`.

---

## 🛠️ Project Structure

```
first-game/
├── main.py                 # Entry point and main menu
├── config.py               # Hardware pin constants and quiz data loader
├── hardware.py             # LED/Button abstraction layer
├── quiz.py                 # Shared input and answer utilities
├── questions.json          # All quiz questions and difficulty settings
└── modes/
    ├── __init__.py
    ├── single_player.py    # 1-player game logic
    └── two_player.py       # 2-player competitive game logic
```

---

## 🧪 Development & Testing Guide

When running on a PC without `gpiozero`, the game safely mocks all hardware interactions. Here is what to expect:

### LED Simulation

LED states are printed directly to the terminal, including GPIO pin numbers so you can trace physical hardware behaviour:

| Terminal Output | What it means |
|---|---|
| `[LED 6 ON]` / `[LED 6 OFF]` | Player 1 indicator — leftmost LED |
| `[LED 19 BLINK on=0.5s off=0.5s]` | Timer LED heartbeat — waiting for a buzz |
| `[LED 19 BLINK on=0.2s off=0.2s]` | Timer LED frantic — player is answering |
| `[LED 11 ON]` / `[LED 11 OFF]` | Player 2 indicator — rightmost LED |

### Button Simulation (2 Player Mode)

Physical button presses are automated on PC to allow the full game loop to be tested. The game randomises which player "buzzes in" using a delay of 0.5s to 2.0s to mimic human reaction times. You will not be prompted to press a button — simply watch the simulation play out.

### Question Timer

On a real Raspberry Pi, `select` is used to interrupt standard input on timeout. On PC, `input()` blocks until you press Enter. To test the "Time's Up" logic, run the game on a Pi and wait without typing when a question appears.

---

## 🧪 Quick Verification Tests

Run these commands from the project root to verify each module is working correctly before running the full game:

**1. Verify data loader:**
```bash
python3 -c "from config import QUIZ_DATA, STEAL_TIME; print(STEAL_TIME); print(list(QUIZ_DATA.keys()))"
```
Expected:
```
5
['A', 'B', 'C']
```

**2. Verify hardware simulation layer:**
```bash
python3 -c "from hardware import set_all_leds, set_timer_led, led_p1; set_all_leds('on'); set_timer_led(fast=True); led_p1.off()"
```
Expected:
```
[LED 6 ON]
[LED 19 ON]
[LED 11 ON]
[LED 19 BLINK on=0.2s off=0.2s]
[LED 6 OFF]
```

**3. Verify answer matching:**
```bash
python3 -c "from quiz import answer_check; print(answer_check('The Nile River', 'nile')); print(answer_check(None, 'nile')); print(answer_check('amazon', 'nile'))"
```
Expected:
```
True
False
False
```

**4. Verify game mode imports:**
```bash
python3 -c "from modes.single_player import play_single_player; from modes.two_player import play_two_player; print('Import OK')"
```
Expected:
```
Import OK
```

---

> Press `Ctrl+C` at any time to exit the game. All hardware LEDs will be safely powered down on exit.
