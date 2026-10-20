# Casio CG100 Games
 
Thirteen games written in MicroPython that run natively on a Casio CG100 graphing calculator. No emulator, no add-ins, just the built-in Python app. The repo also includes [gpSP](#gba-emulator-gpsp), a Game Boy Advance emulator add-in for the CG50 and CG100.
 
<!-- Add a GIF or photo of a game running on the calculator here. This is the single most important thing on the page. -->
<!-- ![Flappy Bird running on a Casio CG100](media/flappy.gif) -->
 
## Games
 
| File | Game | What's interesting |
| --- | --- | --- |
| `flap2048.py` | **2048 Flappy** | An original hybrid. Your bird carries a number, and each wall is a column of powers of two. Fly through the slot matching your number to double it. Reach 2048 to win. |
| `football.py` + `footlib.py` | **Football** | FIFA-style 1-v-1 match on a striped pitch: dribble, shoot, and tackle a CPU striker, beat its goalkeeper, and win before the 90-minute clock runs out. |
| `space.py` | **Space Shooter** | Fly a ship along the bottom of a starfield and shoot down waves of aliens before they get through. Waves get bigger and faster as your score climbs. |
| `halloween.py` | **Trick or Treat** | Catch falling sweets in your pumpkin bucket under a full moon, but dodge the ghosts. More sweets fall, and faster, as your score goes up. |
| `pacman.py` + `paclib.py` | **Pac-Man** | A 27 x 22 maze with 250 dots, power pellets, a wrap-around tunnel, and four ghosts that each chase differently. Eat a power pellet to turn them blue and chase them back. |
| `tetris.py` | **Tetris** | All seven pieces with rotation and wall kicks, soft and hard drop, line clears that speed the game up, and a next-piece preview. |
| `breakout.py` | **Breakout** | Six rows of bricks, a paddle that sets the bounce angle by where the ball lands, and faster levels once a wall is cleared. Easy mode has a slower ball, a wider paddle and five lives; Hard has three lives. |
| `mines.py` | **Minesweeper** | 16 x 8 board with 20 mines. The first square you open is always safe, empty areas open up on their own, and opening a number whose flags are all placed clears its neighbours. |
| `connect4.py` | **Connect Four** | Two-player or vs computer at three levels. Hard searches seven moves ahead with alpha-beta pruning. |
| `tictactoe.py` | **Tic-Tac-Toe** | Two-player or vs computer, with three difficulty levels. Impossible mode uses minimax with alpha-beta pruning. |
| `game2048.py` | **2048** | Full 4x4 slide-and-merge with coloured tiles, scoring and game-over detection. |
| `flappybird.py` | **Flappy Bird** | Gravity, scrolling pipes, collision detection, pause and restart. |
| `snake.py` | **Snake** | Classic grid snake with growing tail, random food and self-collision. Easy mode moves at about half the speed of Hard. |
 
## Install
 
1. Connect the CG100 to your computer over USB and select the storage/USB flash option on the calculator.
2. Copy any of the `.py` files to the calculator's root storage. Pac-Man and Football are two files each: copy `pacman.py` with `paclib.py`, and `football.py` with `footlib.py`, then run `pacman.py` or `football.py`.
3. Eject safely, open the **Python** app, select the file and run it.

File names must start with a letter. Running a script makes the Python app import it as a module (`from <name> import *`), and a module name such as `2048` is a syntax error, so the game never starts. That is why the 2048 games are called `game2048.py` and `flap2048.py`.

## Controls
 
The games read raw key codes from `casioplot.getkey()`. Each code is the key's row and column on the keypad.
 
| Action | Key code | Used in |
| --- | --- | --- |
| Up / Down / Left / Right | 14 / 34 / 23 / 25 (arrow keys) | All except Tic-Tac-Toe and the two Flappy games |
| OK | 24 | Everything: flap, select, drop, open |
| EXE | 95 | Same as OK; flag a square in Minesweeper |
| Number keys 1 to 9 | 81 82 83 / 71 72 73 / 61 62 63 | Tic-Tac-Toe squares, Connect Four columns, menu choices |
| Pause | 36 | Flappy Bird |
| Quit | 12 | All games |
 
Per game:

- **Tetris**: Left/Right move, Up rotates, Down soft drops, OK or EXE hard drops.
- **Snake** and **Breakout**: press 1 for Easy or 2 for Hard on the start screen.
- **Breakout**: Left/Right move the paddle, OK, EXE or Up launches the ball.
- **Minesweeper**: arrows move, OK opens a square, EXE places or removes a flag.
- **Football**: arrows run (you're blue); touch the ball to dribble it, OK or EXE shoots the way you're facing, and run into the CPU to try to win the ball back. You kick off first.
- **Space Shooter**: Left/Right fly, OK, EXE or Up fires (up to three shots on screen).
- **Trick or Treat**: Left/Right move the bucket. Sweets score 10; catching a ghost loses a life.
- **Pac-Man**: arrows steer. Pac-Man keeps going until a wall, and turns at the next opening in the direction you last pressed. Press an arrow to start each life.
- **Connect Four**: Left/Right and OK, or press 1 to 7 to drop straight into that column.
- **Tic-Tac-Toe**: press the number key in the matching position. The board stays on screen the whole game.

The number keys are laid out like the board:

```
7 8 9
4 5 6
1 2 3
```

After a game ends, OK or EXE plays again (Snake and Breakout go back to their start screen) and key 12 quits. Tic-Tac-Toe and Connect Four keep a running score between rounds.
 
## Design notes
 
**Tic-Tac-Toe AI.** Three levels that trade search for rules. Easy plays randomly. Medium takes a winning move, blocks yours, then prefers the centre. Impossible runs a full minimax search with alpha-beta pruning, scoring wins as `10 - depth` so it takes the fastest win and delays any loss. The game used to draw with `turtle` and read moves with `input()`, which switches the calculator back to the shell, so the board only flashed up between moves. It now draws with `casioplot` and reads keys with `getkey()`, so the board never leaves the screen.

**Connect Four AI.** All three levels run a negamax search with alpha-beta pruning, two, four and seven moves deep, trying centre columns first and scoring wins by how soon they come. Change `DP` at the top of the file to make it think deeper or faster.

**Working within the calculator's limits.** The CG100 runs MicroPython 1.9.4 and its editor accepts at most 300 lines of up to 255 characters, so the code uses short identifiers and compact formatting. Every file here is under 160 lines. Rendering is done pixel by pixel through `casioplot`, with each frame drawn off-screen and pushed with `show_screen()`, and frame timing handled with simple delay loops (there is no `time` module). Tetris, Breakout and Minesweeper only redraw what moved instead of clearing the screen each frame, and 2048 only repaints tiles that changed, which keeps them quick even though they draw far more than Snake or Flappy Bird. If a game feels too fast or slow on your calculator, change the delay constant `D` at the top of `tetris.py` or `breakout.py`.

**Memory.** The calculator compiles a whole file before running it, and the Python heap is small: Tic-Tac-Toe and Connect Four first failed to start because compiling them needed more memory than the calculator has. Every game is now checked on a desktop build of MicroPython 1.9.4 (the CG100's version) and must run within a 31 KB heap there, the same as the original Tic-Tac-Toe, which is known to run on the calculator. Long functions and big lists cost the most, so boards are `bytearray`s and Pac-Man is split into two files, compiled one at a time. If a game you edit stops starting, it has most likely grown past this budget.
 
**2048 Flappy.** Each wall is eight blocks of powers of two (2 to 256), with one slot swapped for your current value. Collision checks which block the bird's centre passes through, so the challenge is both steering and reading the wall in time.

## GBA emulator (gpSP)

[`gpsp/`](gpsp) is a git submodule containing [gpSP for CASIO](https://github.com/KaraRyougi/gpsp-sh4-jit) by KaraRyougi, a Game Boy Advance emulator add-in for the fx-CG50 / Graph 90+E and fx-CG100 / Graph Math+ with an SH-4 dynamic recompiler. The submodule points at [a fork](https://github.com/ayush-jha-ai/gpsp-sh4-jit) that adds:

- **Cheats**: CodeBreaker codes from a `.cht` file next to each ROM, switched on and off from the CHEATS menu.
- **Save+Exit**: save a state and quit in one step, from the menu or a hotkey.
- **Separate save files for similar ROM names**: `Pokemon FireRed` and `Pokemon Emerald` no longer overwrite each other's saves. Older saves are still picked up.
- **CI**: GitHub Actions runs the emulator's host test suite with GCC and Clang on every push.

Clone with `git clone --recurse-submodules`, or run `git submodule update --init` in an existing clone. Installation, controls and build instructions are in [gpsp/README.md](gpsp/README.md). gpSP is a C add-in (`.g3a`), not a Python script, and it needs a ROM you are entitled to use.
 
## Requirements
 
- Casio CG100 (or another Casio model with Python and `casioplot`; untested elsewhere)
- `connect4.py` also uses the `math` module, which the CG100 includes

## Licence
 
The games are MIT licensed (see [LICENSE](LICENSE)). gpSP in `gpsp/` is a separate project under the GNU General Public License v3; see [gpsp/LICENSE](gpsp/LICENSE).
