from casioplot import *
from random import randint

# Constants
WIDTH = 384
HEIGHT = 192

# Colours
BLACK = (0, 0, 0)
YELLOW = (249, 241, 36)
GREEN = (117, 191, 48)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# Keys
KEY_EXIT = 12
KEY_PAUSE = 36
CONTINUE_KEYS = (24, 95)

# Rectangle class
class Rect:
    def __init__(self, left, top, right, bottom, colour=BLACK):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.colour = colour

    def draw(self):
        for x in range(self.left, self.right + 1):
            set_pixel(x, self.top, self.colour)
            set_pixel(x, self.bottom, self.colour)

        for y in range(self.top + 1, self.bottom):
            set_pixel(self.left, y, self.colour)
            set_pixel(self.right, y, self.colour)

    def move(self, amount_x, amount_y):
        self.left += amount_x
        self.right += amount_x
        self.top += amount_y
        self.bottom += amount_y

# Bird class
class Bird(Rect):
    def __init__(self, size_x=20, size_y=20, start_x=60, start_y=90):
        half_x = size_x // 2
        half_y = size_y // 2

        Rect.__init__(
            self,
            start_x - half_x,
            start_y - half_y,
            start_x + half_x,
            start_y + half_y,
            YELLOW
        )

        self.velocity = 0

    def flap(self, strength):
        self.velocity = -strength

    def update(self, gravity):
        self.velocity += gravity

        # Limit falling speed
        if self.velocity > 8:
            self.velocity = 8

        self.move(0, int(self.velocity))

    def is_crashed(self):
        # Hit floor
        if self.bottom >= HEIGHT - 1:
            return True

        # Hit ceiling
        if self.top <= 0:
            return True

        return False

# Pipe class
class Pipe:
    def __init__(self, xpos, gap_y, gap_size):
        self.xpos = xpos
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.cleared = False

        half_gap = gap_size // 2

        self.top = Rect(
            xpos - 20,
            0,
            xpos + 20,
            gap_y - half_gap,
            GREEN
        )

        self.bottom = Rect(
            xpos - 20,
            gap_y + half_gap,
            xpos + 20,
            HEIGHT - 1,
            GREEN
        )

    def move(self, speed):
        self.xpos -= speed
        self.top.move(-speed, 0)
        self.bottom.move(-speed, 0)

    def check_collision(self, bird):
        horizontal_collision = (
            bird.right >= self.top.left and
            bird.left <= self.top.right
        )

        vertical_collision = (
            bird.top <= self.top.bottom or
            bird.bottom >= self.bottom.top
        )

        if horizontal_collision and vertical_collision:
            return True

        return False

    def bird_passed(self, bird):
        if self.top.right < bird.left and not self.cleared:
            self.cleared = True
            return True

        return False

    def is_off_screen(self):
        return self.top.right < 0

    def draw(self):
        self.top.draw()
        self.bottom.draw()

# Draw centred text
def centre_text(text, y=85, colour=BLACK, size="large"):
    if size == "large":
        x_adjust = 9
    elif size == "medium":
        x_adjust = 5
    else:
        x_adjust = 4

    x = 191 - (len(text) * x_adjust)

    draw_string(
        x,
        y,
        text,
        colour,
        size
    )

# Difficulty menu
def get_difficulty():
    clear_screen()

    centre_text(
        "FLAPPY BIRD",
        25,
        YELLOW,
        "large"
    )

    draw_string(
        110,
        75,
        "1 - Easy",
        BLACK,
        "medium"
    )

    draw_string(
        110,
        100,
        "2 - Medium",
        BLACK,
        "medium"
    )

    draw_string(
        110,
        125,
        "3 - Hard",
        BLACK,
        "medium"
    )

    show_screen()

    while True:
        key = getkey()

        if key == 1:
            return 1

        elif key == 2:
            return 2

        elif key == 3:
            return 3

# Get game settings
def get_settings(difficulty):
    if difficulty == 1:
        gravity = 1
        flap_strength = 6
        pipe_speed = 3
        gap_size = 80

    elif difficulty == 2:
        gravity = 1
        flap_strength = 7
        pipe_speed = 4
        gap_size = 70

    else:
        gravity = 1
        flap_strength = 7
        pipe_speed = 5
        gap_size = 60

    return gravity, flap_strength, pipe_speed, gap_size

# Create a new pipe
def create_pipe(x, gap_size):
    half_gap = gap_size // 2

    minimum = 30 + half_gap
    maximum = HEIGHT - 30 - half_gap

    gap_y = randint(
        minimum,
        maximum
    )

    return Pipe(
        x,
        gap_y,
        gap_size
    )

# Draw entire game
def draw_game(bird, pipes, score, high_score):
    clear_screen()

    for pipe in pipes:
        pipe.draw()

    bird.draw()

    draw_string(
        5,
        5,
        "Score: " + str(score),
        BLACK,
        "small"
    )

    draw_string(
        120,
        5,
        "Best: " + str(high_score),
        BLACK,
        "small"
    )

    show_screen()

# Pause screen
def pause_game(score):
    centre_text(
        "PAUSED",
        70,
        BLUE,
        "large"
    )

    centre_text(
        "Score: " + str(score),
        105,
        BLACK,
        "medium"
    )

    show_screen()

    # Wait for flap/continue key
    while True:
        key = getkey()

        if key in CONTINUE_KEYS:
            return

# Calculate current pipe speed
def get_pipe_speed(start_speed, score):
    speed = start_speed

    # Increase speed every 5 pipes
    speed += score // 5

    # Maximum speed
    if speed > 8:
        speed = 8

    return speed

# Calculate current gap size
def get_gap_size(start_gap, score):
    # Make the gap smaller as score increases
    gap = start_gap - ((score // 5) * 4)

    # Prevent impossible gaps
    if gap < 45:
        gap = 45

    return gap

# Play one game
def play_game(difficulty, high_score):
    gravity, flap_strength, start_speed, start_gap = get_settings(
        difficulty
    )

    bird = Bird()
    score = 0
    playing = True

    pipes = [
        create_pipe(220, start_gap),
        create_pipe(380, start_gap)
    ]

    draw_game(
        bird,
        pipes,
        score,
        high_score
    )

    while playing:
        key = getkey()

        # Flap
        if key in CONTINUE_KEYS:
            bird.flap(flap_strength)

        # Pause
        elif key == KEY_PAUSE:
            pause_game(score)

        # Exit game
        elif key == KEY_EXIT:
            return score, high_score, False

        # Update bird physics
        bird.update(gravity)

        # Increase difficulty gradually
        pipe_speed = get_pipe_speed(
            start_speed,
            score
        )

        current_gap = get_gap_size(
            start_gap,
            score
        )

        # Move pipes
        for pipe in pipes:
            pipe.move(pipe_speed)

        # Check pipe collisions and scoring
        for pipe in pipes:
            if pipe.check_collision(bird):
                playing = False

            if pipe.bird_passed(bird):
                score += 1

                if score > high_score:
                    high_score = score

        # Check floor/ceiling collision
        if bird.is_crashed():
            playing = False

        # Remove old pipes
        new_pipes = []

        for pipe in pipes:
            if not pipe.is_off_screen():
                new_pipes.append(pipe)

        pipes = new_pipes

        # Add new pipe when needed
        if len(pipes) == 0:
            pipes.append(
                create_pipe(
                    WIDTH + 20,
                    current_gap
                )
            )

        else:
            last_pipe = pipes[len(pipes) - 1]

            if last_pipe.xpos < WIDTH - 160:
                pipes.append(
                    create_pipe(
                        WIDTH + 20,
                        current_gap
                    )
                )

        # Draw next frame
        draw_game(
            bird,
            pipes,
            score,
            high_score
        )

    return score, high_score, True

# Game over screen
def game_over_screen(score, high_score):
    clear_screen()

    centre_text(
        "GAME OVER",
        40,
        RED,
        "large"
    )

    centre_text(
        "Score: " + str(score),
        85,
        BLACK,
        "medium"
    )

    centre_text(
        "Best: " + str(high_score),
        110,
        BLACK,
        "medium"
    )

    centre_text(
        "1 - Play Again",
        140,
        BLACK,
        "medium"
    )

    centre_text(
        "0 - Quit",
        165,
        BLACK,
        "medium"
    )

    show_screen()

    while True:
        key = getkey()

        if key == 1:
            return True

        elif key == 0:
            return False

# Main function
def main():
    high_score = 0
    running = True

    while running:
        difficulty = get_difficulty()

        score, high_score, finished = play_game(
            difficulty,
            high_score
        )

        if finished:
            running = game_over_screen(
                score,
                high_score
            )
        else:
            running = False

    clear_screen()

    centre_text(
        "Thanks for playing!",
        85,
        BLUE,
        "medium"
    )

    show_screen()

# Program entry point
if __name__ == "__main__":
    main()
