from tkinter import *
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    my_label.config(text="TIMER", fg=GREEN)
    checkmark.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        my_label.config(text="LONG BREAK", fg=RED)
        count_down(long_break_sec)
        messagebox.showinfo("Time for a Long Break!", f"Congrats! You've earned a {LONG_BREAK_MIN}-minute long break 🎉")
    elif reps % 2 == 0:
        my_label.config(text="SHORT BREAK", fg=PINK)
        count_down(short_break_sec)
        messagebox.showinfo("Short Break", f"Time for a {SHORT_BREAK_MIN}-minute short break ☕")
    else:
        my_label.config(text="WORK", fg=GREEN)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = reps // 2
        for _ in range(work_sessions):
            marks += "✓"
        checkmark.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

my_label = Label(window, text="TIMER", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 60, "bold"))
my_label.grid(column=1, row=0)

canvas = Canvas(window, width=300, height=300, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file=r"C:\Users\meet\OneDrive\Desktop\MEET\Tkinter Projects\tomato.png")
canvas.create_image(150, 150, image=tomato_image)
canvas.grid(column=1, row=1)
timer_text = canvas.create_text(155, 180, text="00:00", font=(FONT_NAME, 35, "bold"), fill="white")

start_button = Button(window, text="START", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(window, text="RESET", command=reset_timer)
reset_button.grid(column=2, row=2)

checkmark = Label(window, text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
checkmark.grid(column=1, row=3)

window.mainloop()
