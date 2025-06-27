Here's a complete and professional `README.md` for your **Sneke Game** based on the code you provided:

---

# 🐍 Snake Game

**Snake Game** is a visually enhanced and feature-rich take on the classic Snake game made using **Python** and **Pygame**. Navigate your snake across a grid to eat apples, grow longer, unlock skins, and track your high scores — all while avoiding tail collisions and deadly walls!

## 🎮 Features

- ✅ Classic Snake Mechanics
- 🍎 Apple Collecting System (easy vs hard mode affects apple count and scoring)
- 🎨 Unlockable & Selectable Skins (with in-game currency system)
- 🔐 Score & Skin Progress Saving via encrypted local file
- ⛔ Death Types (Tail Touch or Wall Hit)
- ⏸️ Pause Menu (press `Esc`)
- 🧠 Difficulty Toggle (Easy vs Hard)
- 🏆 Achievement System
- 👤 Credits Page
- 📱 Fully Interactive UI with mouse-based buttons

---


## 🚀 How to Run

### 🔧 Requirements

* Python 3.x
* Pygame

### 📥 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ReubenTRG/Snake-Game.git
   cd Snake-Game
   ```
2. Install dependencies:

   ```bash
   pip install pygame
   ```
3. Run the game:

   ```bash
   python SnakeGame.py
   ```

---

## 🕹️ Controls

| Action         | Key(s)          |
| -------------- | --------------- |
| Move Up        | `W` / `↑` arrow |
| Move Down      | `S` / `↓` arrow |
| Move Left      | `A` / `←` arrow |
| Move Right     | `D` / `→` arrow |
| Pause/Resume   | `Esc`           |
| Select Buttons | `Mouse Click`   |

---

## 💾 Saved Data

Game progress is automatically saved in a local encrypted file named `SavedData.txt` containing:

* Apples eaten (Score)
* Equipped Skin index
* Unlocked Skins
* Difficulty setting

If corruption or parsing errors occur, the save will reset automatically.

---

## 🧩 Skins

Unlockable skins include:

* Original (Default)
* Red
* Purple
* Lime
* Gold (Premium)

Each skin has its own unique color palette for the snake's head and body.

---

## 🏅 Achievements

* 🎖️ **Knight in Shining Armor**: Unlock Gold Skin
* 🎖️ **All Skins Collected**: Unlock all available skins

---

## 🧠 Game Modes

* **Easy Mode**: 3 apples spawn at once; allows screen wrapping
* **Hard Mode**: 1 apple spawns; hitting wall causes death; earns 2× score per apple

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more info.

---

## ✨ Credits

**Developed by:** TRG
🎨 UI, Game Logic, and all features were hand-crafted using `pygame`.

---

## 🧠 Notes

* Sound effects play when apples are eaten (`Bite.mp3`)
* Ensure `Bite.mp3` exists in the same directory for audio playback
* Full screen/chunky pixel aesthetic designed for fun and learning

---

## 💡 Want to Contribute?

Feel free to fork and PR! You can add:

* New skins
* More achievements
* Sound/music enhancements
* Score leaderboard

---

Enjoy the game and happy coding! 🐍🎮

```

---

Let me know if:
- You want this broken into multiple files
- You want to include a screenshot or GIF
- You want the README converted to HTML or formatted for PyPI release

I'll help tailor it as needed!
