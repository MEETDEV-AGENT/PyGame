import turtle
import pandas

# Set up screen
screen = turtle.Screen()
screen.title("U.S. States Game")

image = r"C:\Users\meet\OneDrive\Desktop\MEET\Pandas Project\US STATE GAMES\blank_states_img.gif"

screen.addshape(image)
turtle.shape(image)

# Load data
data = pandas.read_csv(
    r"C:\Users\meet\OneDrive\Desktop\MEET\Pandas Project\US STATE GAMES\50_states.csv"
)

all_states = data.state.to_list()
guessed_states = []

# Main game loop
while len(guessed_states) < 50:
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="What's another state's name? (or type 'Exit' to quit)"
    )

    if answer_state is None:
        break

    answer_state = answer_state.title()

    if answer_state == "Exit":
        break

    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)

        state_data = data[data.state == answer_state]

        writer = turtle.Turtle()
        writer.hideturtle()
        writer.penup()
        writer.goto(
            int(state_data.x.iloc[0]),
            int(state_data.y.iloc[0])
        )
        writer.write(answer_state)

# Save missed states
missed_states = [
    state for state in all_states
    if state not in guessed_states
]

missed_data = pandas.DataFrame(missed_states)
missed_data.to_csv("states_to_learn.csv")

screen.exitonclick()

