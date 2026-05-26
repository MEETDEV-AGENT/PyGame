from turtle import Turtle, Screen
import random
import time

# Screen setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("white")
screen.title("Turtle Crossing Game")
screen.tracer(0)

# Constants
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
Y_POSITIONS = [-250, -200, -150, -100, -50, 0, 50, 100, 150, 200, 250]
USED_Y_POSITIONS = []
CAR_WIDTH = 2
CAR_HEIGHT = 1
INITIAL_SPEED = 2
car_speed = INITIAL_SPEED
LEVELS = 5
current_level = 1
game_over = False
all_cars = []

# Player turtle setup
player = Turtle("turtle")
player.penup()
player.goto(0, -280)
player.setheading(90)

# Level display
level_display = Turtle()
level_display.hideturtle()
level_display.penup()
level_display.goto(-250, 260)
level_display.write(f"Level: {current_level}", font=("Arial", 16, "bold"))

# Message display
message = Turtle()
message.hideturtle()
message.penup()

# Keyboard control
def move_up():
    if not game_over:
        player.forward(10)

screen.listen()
screen.onkey(move_up, "Up")

# Create a car at a random y-position
def create_car():
    global USED_Y_POSITIONS
    if len(USED_Y_POSITIONS) >= len(Y_POSITIONS):
        USED_Y_POSITIONS = []
    available_positions = list(set(Y_POSITIONS) - set(USED_Y_POSITIONS))
    y = random.choice(available_positions)
    USED_Y_POSITIONS.append(y)

    car = Turtle("square")
    car.penup()
    car.color(random.choice(COLORS))
    car.shapesize(stretch_wid=CAR_HEIGHT, stretch_len=CAR_WIDTH)
    car.goto(x=-300, y=y)
    all_cars.append(car)

# Collision detection
def detect_collision():
    for car in all_cars:
        if player.distance(car) < 25:
            return True
    return False

# Reset player position
def reset_player():
    player.goto(0, -280)

# Main game loop
last_spawn_time = time.time()
last_speed_boost_time = time.time()
next_spawn_interval = random.uniform(0.1, 0.3)

while True:
    screen.update()
    current_time = time.time()

    if game_over:
        break

    # Create car randomly
    if current_time - last_spawn_time >= next_spawn_interval:
        create_car()
        last_spawn_time = current_time
        next_spawn_interval = random.uniform(0.1, 0.3)

    # Move cars
    for car in all_cars:
        car.forward(car_speed)

    # Check collision
    if detect_collision():
        message.goto(0, 0)
        message.write("Game Over!", align="center", font=("Courier", 24, "bold"))
        game_over = True
        break

    # Check if player reached top
    if player.ycor() > 280:
        current_level += 1
        if current_level > LEVELS:
            message.goto(0, 0)
            message.write("You Won!", align="center", font=("Courier", 24, "bold"))
            game_over = True
            break
        else:
            car_speed += 0.3
            reset_player()
            level_display.clear()
            level_display.write(f"Level: {current_level}", font=("Courier", 16, "bold"))

    time.sleep(0.01)
