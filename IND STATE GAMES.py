import turtle
import tkinter as tk
import pandas as pd

# ---------------- SCREEN ---------------- #

screen = turtle.Screen()
screen.title("India States Game")

image = r"C:\Users\meet\OneDrive\Desktop\MEET\Pandas Project\IND STATE GAMES\political-map.gif"

screen.addshape(image)
turtle.shape(image)

# ---------------- DATA ---------------- #

data = pd.read_csv(r"C:\Users\meet\OneDrive\Desktop\MEET\Pandas Project\IND STATE GAMES\indian_states.csv")

all_states = data.state.to_list()
guessed_states = []

# ---------------- WRITER ---------------- #

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

# ---------------- TKINTER INPUT BOX ---------------- #

canvas = screen.getcanvas()

root = canvas.winfo_toplevel()

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(side="left", padx=10, pady=5)

# ---------------- SUBMIT FUNCTION ---------------- #

def check_answer():

    answer = entry.get().strip().title()

    entry.delete(0, tk.END)

    if answer in all_states and answer not in guessed_states:

        guessed_states.append(answer)

        state_data = data[data.state == answer]

        state_writer = turtle.Turtle()
        state_writer.hideturtle()
        state_writer.penup()

        state_writer.goto(
            int(state_data.x.iloc[0]),
            int(state_data.y.iloc[0])
        )

        state_writer.write(
            answer,
            align="center",
            font=("Arial", 8, "normal")
        )

        screen.title(
            f"{len(guessed_states)}/{len(all_states)} Correct"
        )

# ---------------- BUTTON ---------------- #

button = tk.Button(
    root,
    text="Submit",
    command=check_answer
)

button.pack(side="left", padx=5)

# Press Enter to submit
entry.bind("<Return>", lambda event: check_answer())

screen.mainloop()
