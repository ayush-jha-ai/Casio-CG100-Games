# Casio CG100 Games
 
Five games written in MicroPython that run natively on a Casio CG100 graphing calculator. No emulator, no add-ins, just the built-in Python app.
 
<!-- Add a GIF or photo of a game running on the calculator here. This is the single most important thing on the page. -->
<!-- ![Flappy Bird running on a Casio CG100](media/flappy.gif) -->
 
## Games
 
| File | Game | What's interesting |
| --- | --- | --- |
| `2048flappy.py` | **2048 Flappy** | An original hybrid. Your bird carries a number, and each wall is a column of powers of two. Fly through the slot matching your number to double it. Reach 2048 to win. |
| `tictactoe.py` | **Tic-Tac-Toe** | Two-player or vs computer, with three difficulty levels. Impossible mode uses minimax with alpha-beta pruning. |
| `2048.py` | **2048** | Full 4x4 slide-and-merge with scoring and game-over detection. |
| `flappybird.py` | **Flappy Bird** | Gravity, scrolling pipes, collision detection, pause and restart. |
| `snake.py` | **Snake** | Classic grid snake with growing tail, random food and self-collision. |
 
## Install
 
1. Connect the CG100 to your computer over USB and select the storage/USB flash option on the calculator.
2. Copy any of the `.py` files to the calculator's root storage.
3. Eject safely, open the **Python** app, select the file and run it.
## Controls
 
The games read raw key codes from `casioplot.getkey()`.
 
| Action | Key code | Used in |
| --- | --- | --- |
| Up / Down / Left / Right | 14 / 34 / 23 / 25 (arrow keys) | Snake, 2048 |
| Flap | 24 or 95 (ok button) | Flappy Bird, 2048 Flappy |
| Pause | 36 | Flappy Bird |
| Quit | 12 | 2048, Flappy Bird, 2048 Flappy |
| Restart after game over | 24 or 95 | Flappy Bird, 2048 Flappy |
 
Tic-Tac-Toe runs in the console: choose a mode and difficulty, then enter positions 1 to 9 laid out like a numpad.
 
```
7 8 9
4 5 6
1 2 3
```
 
## Design notes
 
**Tic-Tac-Toe AI.** Three levels that trade search for rules. Easy plays randomly. Medium takes a winning move, blocks yours, then prefers the centre. Impossible runs a full minimax search with alpha-beta pruning, scoring wins as `10 - depth` so it takes the fastest win and delays any loss.
 
**Working within the calculator's limits.** The CG100 runs MicroPython with very limited memory, so the code uses short identifiers and compact formatting to keep source size and parse-time memory down. This is deliberate, not a style choice. Rendering is done pixel by pixel through `casioplot`, with each frame drawn off-screen and pushed with `show_screen()`, and frame timing handled with simple delay loops.
 
**2048 Flappy.** Each wall is eight blocks of powers of two (2 to 256), with one slot swapped for your current value. Collision checks which block the bird's centre passes through, so the challenge is both steering and reading the wall in time.
 
## Requirements
 
- Casio CG100 (or another Casio model with Python and `casioplot`; untested elsewhere)
- `tictactoe.py` also needs the `turtle` module
## Licence
 
MIT
