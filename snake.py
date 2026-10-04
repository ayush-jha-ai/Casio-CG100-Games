import casioplot
import random

# Constants
WIDTH = 384
HEIGHT = 192
CELL_SIZE = 8
TOP_MARGIN = 24
COLS = WIDTH // CELL_SIZE
ROWS = (HEIGHT - TOP_MARGIN) // CELL_SIZE

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (180, 180, 180)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Calculator keys
KEY_UP = "14"
KEY_LEFT = "23"
KEY_RIGHT = "25"
KEY_DOWN = "34"

class Snake:
    def __init__(self):
        start_x = COLS // 2
        start_y = ROWS // 2
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.growing = False

    def get_head(self):
        return self.body[0]

    def move(self):
        self.direction = self.next_direction
        head = self.get_head()
        new_head = (
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        )
        self.body.insert(0, new_head)

        if self.growing:
            self.growing = False
        else:
            self.body.pop()

    def grow(self):
        self.growing = True

    def set_direction(self, new_direction):
        # Prevent the snake reversing directly into itself
        if (
            self.direction[0] + new_direction[0] == 0 and
            self.direction[1] + new_direction[1] == 0
        ):
            return False

        self.next_direction = new_direction
        return True

    def check_collision(self):
        head = self.get_head()

        # Wall collision
        if head[0] < 0 or head[0] >= COLS:
            return True

        if head[1] < 0 or head[1] >= ROWS:
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False

class Food:
    def __init__(self, snake):
        self.position = self.spawn(snake)

    def spawn(self, snake):
        free_cells = []

        for y in range(ROWS):
            for x in range(COLS):
                if (x, y) not in snake.body:
                    free_cells.append((x, y))

        if len(free_cells) == 0:
            return None

        return random.choice(free_cells)

    def respawn(self, snake):
        self.position = self.spawn(snake)

def draw_cell(x, y, color):
    screen_x = x * CELL_SIZE
    screen_y = TOP_MARGIN + y * CELL_SIZE

    for i in range(CELL_SIZE - 1):
        for j in range(CELL_SIZE - 1):
            casioplot.set_pixel(
                screen_x + i,
                screen_y + j,
                color
            )

def draw_snake(snake):
    head = snake.get_head()

    draw_cell(
        head[0],
        head[1],
        BLUE
    )

    for segment in snake.body[1:]:
        draw_cell(
            segment[0],
            segment[1],
            GREEN
        )

def draw_food(food):
    if food.position is not None:
        draw_cell(
            food.position[0],
            food.position[1],
            RED
        )

def draw_border():
    for x in range(WIDTH):
        casioplot.set_pixel(
            x,
            TOP_MARGIN - 1,
            GREY
        )

def draw_score(score, high_score):
    casioplot.draw_string(
        5,
        4,
        "Score: " + str(score),
        BLACK,
        "small"
    )

    casioplot.draw_string(
        120,
        4,
        "Best: " + str(high_score),
        BLACK,
        "small"
    )

def draw_game(snake, food, score, high_score):
    casioplot.clear_screen()

    draw_border()
    draw_snake(snake)
    draw_food(food)
    draw_score(score, high_score)

    casioplot.show_screen()

def get_key():
    return str(casioplot.getkey())

def handle_input(snake):
    key = get_key()

    if key == KEY_UP:
        snake.set_direction(UP)

    elif key == KEY_DOWN:
        snake.set_direction(DOWN)

    elif key == KEY_LEFT:
        snake.set_direction(LEFT)

    elif key == KEY_RIGHT:
        snake.set_direction(RIGHT)

    return key

def get_speed_delay(difficulty, score):
    if difficulty == 1:
        delay = 14

    elif difficulty == 2:
        delay = 10

    else:
        delay = 7

    # Increase speed as score rises
    speed_increase = score // 50
    delay -= speed_increase

    # Prevent game becoming impossibly fast
    if delay < 3:
        delay = 3

    return delay

def show_menu():
    casioplot.clear_screen()

    casioplot.draw_string(
        135,
        25,
        "SNAKE",
        GREEN,
        "large"
    )

    casioplot.draw_string(
        100,
        75,
        "1 - Easy",
        BLACK,
        "medium"
    )

    casioplot.draw_string(
        100,
        100,
        "2 - Medium",
        BLACK,
        "medium"
    )

    casioplot.draw_string(
        100,
        125,
        "3 - Hard",
        BLACK,
        "medium"
    )

    casioplot.show_screen()

    while True:
        key = str(casioplot.getkey())

        if key == "1":
            return 1

        elif key == "2":
            return 2

        elif key == "3":
            return 3

def show_game_over(score, high_score):
    casioplot.clear_screen()

    casioplot.draw_string(
        115,
        45,
        "GAME OVER",
        RED,
        "large"
    )

    casioplot.draw_string(
        130,
        85,
        "Score: " + str(score),
        BLACK,
        "medium"
    )

    casioplot.draw_string(
        130,
        110,
        "Best: " + str(high_score),
        BLACK,
        "medium"
    )

    casioplot.draw_string(
        90,
        145,
        "Press 1 to play again",
        BLACK,
        "small"
    )

    casioplot.draw_string(
        90,
        165,
        "Press 0 to quit",
        BLACK,
        "small"
    )

    casioplot.show_screen()

    while True:
        key = str(casioplot.getkey())

        if key == "1":
            return True

        elif key == "0":
            return False

def play_game(difficulty, high_score):
    snake = Snake()
    food = Food(snake)

    score = 0
    iteration = 0
    game_over = False

    draw_game(
        snake,
        food,
        score,
        high_score
    )

    while not game_over:
        iteration += 1

        handle_input(snake)

        move_delay = get_speed_delay(
            difficulty,
            score
        )

        if iteration % move_delay == 0:
            snake.move()

            # Check collision before drawing
            if snake.check_collision():
                game_over = True
                continue

            # Check food collision
            if snake.get_head() == food.position:
                snake.grow()

                score += 10

                if score > high_score:
                    high_score = score

                food.respawn(snake)

                # Player has filled the board
                if food.position is None:
                    game_over = True

            draw_game(
                snake,
                food,
                score,
                high_score
            )

    return score, high_score

def main():
    high_score = 0
    playing = True

    while playing:
        difficulty = show_menu()

        score, high_score = play_game(
            difficulty,
            high_score
        )

        playing = show_game_over(
            score,
            high_score
        )

    casioplot.clear_screen()

    casioplot.draw_string(
        125,
        80,
        "Thanks for playing!",
        BLUE,
        "medium"
    )

    casioplot.show_screen()

if __name__ == "__main__":
    main()
