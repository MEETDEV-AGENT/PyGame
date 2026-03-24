from turtle import Screen, Turtle
import random
import time
import os

# Constants
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")
BUTTON_FONT = ("Courier", 16, "bold")
RESET_FILE = "high_score.txt"

# Load high score from file
if os.path.exists(RESET_FILE):
    with open(RESET_FILE) as file:
        HIGH_SCORE = int(file.read())
else:
    HIGH_SCORE = 0


# Food class
class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.goto(x, y)


# Snake class
class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        start_x = 0
        for i in range(3):
            self.add_segment(start_x - i * 20, 0)

    def add_segment(self, x=0, y=0):
        segment = Turtle("square")
        segment.color("white")
        segment.penup()
        segment.goto(x, y)
        self.segments.append(segment)

    def extend(self):
        self.add_segment(self.segments[-1].xcor(), self.segments[-1].ycor())

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)
        self.head.forward(20)

    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]


# Scoreboard class
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = HIGH_SCORE
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(RESET_FILE, "w") as file:
                file.write(str(self.high_score))
        self.score = 0
        self.update_scoreboard()


# Reset Button Class
class ResetButton(Turtle):
    def __init__(self, click_callback):
        super().__init__()
        self.click_callback = click_callback
        self.hideturtle()
        self.penup()
        self.color("yellow")
        self.button_coords = (-100, -80, 100, -40)  # x1, y1, x2, y2
        self.draw_button()
        screen.onclick(self.check_click)

    def draw_button(self):
        self.goto(self.button_coords[0], self.button_coords[1])
        self.pendown()
        self.begin_fill()
        for _ in range(2):
            self.forward(self.button_coords[2] - self.button_coords[0])
            self.left(90)
            self.forward(self.button_coords[3] - self.button_coords[1])
            self.left(90)
        self.end_fill()
        self.penup()
        self.goto(0, -65)
        self.color("black")
        self.write("RESET", align="center", font=BUTTON_FONT)

    def check_click(self, x, y):
        x1, y1, x2, y2 = self.button_coords
        if x1 <= x <= x2 and y1 <= y <= y2:
            screen.onclick(None)  # Disable further clicks
            self.clear()
            self.goto(1000, 1000)
            self.click_callback()


# Game Reset Function
def start_game():
    global game_is_on
    snake.reset()
    food.refresh()
    scoreboard.reset()
    screen.listen()
    game_is_on = True


# Game Setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while True:
    while game_is_on:
        screen.update()
        time.sleep(0.1)
        snake.move()

        # Collision with food
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()

        # Collision with wall
        if (
            snake.head.xcor() > 280 or snake.head.xcor() < -280
            or snake.head.ycor() > 280 or snake.head.ycor() < -280
        ):
            game_is_on = False

        # Collision with self
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                game_is_on = False

    # Show Reset Button
    reset_button = ResetButton(start_game)
    screen.update()
    while not game_is_on:
        time.sleep(0.1)
        screen.update()

