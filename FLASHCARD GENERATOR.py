from tkinter import *
from tkinter import ttk
import pandas as pd
import random
import os

# ================= PATHS ================= #

PROJECT_DIR = r"C:\Users\meet\OneDrive\Desktop\MEET\Tkinter Projects"

FRENCH_WORDS = os.path.join(PROJECT_DIR, "french_words.csv")
WORDS_TO_LEARN = os.path.join(PROJECT_DIR, "words_to_learn.csv")

CARD_FRONT = os.path.join(PROJECT_DIR, "card_front.png")
CARD_BACK = os.path.join(PROJECT_DIR, "card_back.png")

RIGHT_IMAGE = os.path.join(PROJECT_DIR, "right.png")
WRONG_IMAGE = os.path.join(PROJECT_DIR, "wrong.png")

# ================= GLOBAL VARIABLES ================= #

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = []
flip_timer = None

# ================= LOAD DATA ================= #

def load_data():
    global to_learn

    try:
        if os.path.exists(WORDS_TO_LEARN):
            data = pd.read_csv(WORDS_TO_LEARN)
        else:
            data = pd.read_csv(FRENCH_WORDS)
            data.to_csv(WORDS_TO_LEARN, index=False)

        to_learn = data.to_dict(orient="records")

    except FileNotFoundError:
        canvas.itemconfig(card_title, text="Error")
        canvas.itemconfig(card_word, text="CSV File Not Found")
        print("Could not find french_words.csv")

# ================= NEXT CARD ================= #

def next_card():
    global current_card, flip_timer

    if len(to_learn) == 0:
        canvas.itemconfig(card_background, image=card_front_image)
        canvas.itemconfig(card_title, text="🎉 Complete!", fill="black")
        canvas.itemconfig(card_word, text="All Words Learned!", fill="black")

        progress_label.config(
            text="✅ Congratulations! You've learned all words."
        )

        progress_bar["value"] = 100
        return

    if flip_timer:
        window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)

    canvas.itemconfig(card_background, image=card_front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")

    update_progress()

    flip_timer = window.after(3000, flip_card)

# ================= FLIP CARD ================= #

def flip_card():
    canvas.itemconfig(card_background, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

# ================= KNOWN WORD ================= #

def is_known():
    global current_card

    if current_card in to_learn:
        to_learn.remove(current_card)

        pd.DataFrame(to_learn).to_csv(
            WORDS_TO_LEARN,
            index=False
        )

    next_card()

# ================= RESET ================= #

def reset_learning():

    if os.path.exists(WORDS_TO_LEARN):
        os.remove(WORDS_TO_LEARN)

    load_data()
    next_card()

# ================= PROGRESS ================= #

def update_progress():

    total_words = pd.read_csv(FRENCH_WORDS).shape[0]

    learned_words = total_words - len(to_learn)

    percentage = int(
        (learned_words / total_words) * 100
    )

    progress_label.config(
        text=f"📘 Learned {learned_words} of {total_words} words ({percentage}%)"
    )

    progress_bar["value"] = percentage

# ================= UI ================= #

window = Tk()
window.title("French Flash Cards")
window.config(
    padx=50,
    pady=50,
    bg=BACKGROUND_COLOR
)

# ---------- Images ---------- #

card_front_image = PhotoImage(file=CARD_FRONT)
card_back_image = PhotoImage(file=CARD_BACK)

right_image = PhotoImage(file=RIGHT_IMAGE)
wrong_image = PhotoImage(file=WRONG_IMAGE)

# ---------- Canvas ---------- #

canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

card_background = canvas.create_image(
    400,
    263,
    image=card_front_image
)

card_title = canvas.create_text(
    400,
    150,
    text="",
    font=("Times New Roman", 40, "italic")
)

card_word = canvas.create_text(
    400,
    263,
    text="",
    font=("Times New Roman", 60, "bold")
)

canvas.grid(
    row=0,
    column=0,
    columnspan=3
)

# ---------- Buttons ---------- #

unknown_button = Button(
    image=wrong_image,
    command=next_card,
    highlightthickness=0,
    bd=0,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR
)

unknown_button.grid(
    row=1,
    column=0
)

correct_button = Button(
    image=right_image,
    command=is_known,
    highlightthickness=0,
    bd=0,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR
)

correct_button.grid(
    row=1,
    column=2
)

# ---------- Progress Section ---------- #

progress_frame = Frame(
    bg=BACKGROUND_COLOR
)

progress_frame.grid(
    row=2,
    column=0,
    columnspan=3,
    pady=10
)

progress_label = Label(
    progress_frame,
    text="📘 Learned 0 of 0 words",
    font=("Arial", 13, "bold"),
    bg=BACKGROUND_COLOR,
    fg="#333333"
)

progress_label.pack()

progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=350,
    mode="determinate"
)

progress_bar.pack(pady=8)

reset_button = Button(
    progress_frame,
    text="🔁 Restart Learning",
    command=reset_learning,
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5
)

reset_button.pack()

# ================= START APP ================= #

load_data()

flip_timer = window.after(
    3000,
    flip_card
)

next_card()

window.mainloop()
