from tkinter import *
from tkinter import messagebox
import random
import json
import os

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not website or not email or not password:
        messagebox.showwarning(
            title="Oops",
            message="Please don't leave any fields empty!"
        )
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=f"Website: {website}\nEmail: {email}\nPassword: {password}\n\nSave?"
    )

    if not is_ok:
        return

    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

    messagebox.showinfo(
        title="Success",
        message="Password saved successfully!"
    )

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get()

    if not website:
        messagebox.showwarning(
            title="Oops",
            message="Please enter a website."
        )
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showerror(
            title="Error",
            message="No Data File Found."
        )

    except json.JSONDecodeError:
        messagebox.showerror(
            title="Error",
            message="Data file is corrupted."
        )

    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]

            messagebox.showinfo(
                title=website,
                message=f"Email: {email}\nPassword: {password}"
            )
        else:
            messagebox.showerror(
                title="Error",
                message=f"No details for {website} found."
            )

# ---------------------------- EXTRA FEATURES ------------------------------- #
def copy_password():
    if password_entry.get():
        window.clipboard_clear()
        window.clipboard_append(password_entry.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="•")
        eye_btn.config(text="👁")
    else:
        password_entry.config(show="")
        eye_btn.config(text="🙈")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.geometry("550x500")
window.resizable(False, False)
window.config(padx=30, pady=20, bg="#F5F5F5")

# ---------------------------- LOGO ------------------------------- #
logo_path = r"C:\Users\meet\OneDrive\Desktop\MEET\Tkinter Projects\logo.png"

canvas = Canvas(
    width=200,
    height=200,
    bg="#F5F5F5",
    highlightthickness=0
)

if os.path.exists(logo_path):
    logo_img = PhotoImage(file=logo_path)
    canvas.create_image(100, 100, image=logo_img)

canvas.grid(row=0, column=0, columnspan=3, pady=(0, 10))

# ---------------------------- LABELS ------------------------------- #
Label(
    text="Website",
    font=("Segoe UI", 10, "bold"),
    bg="#F5F5F5"
).grid(row=1, column=0, sticky="e", pady=5)

Label(
    text="Email / Username",
    font=("Segoe UI", 10, "bold"),
    bg="#F5F5F5"
).grid(row=2, column=0, sticky="e", pady=5)

Label(
    text="Password",
    font=("Segoe UI", 10, "bold"),
    bg="#F5F5F5"
).grid(row=3, column=0, sticky="e", pady=5)

# ---------------------------- ENTRIES ------------------------------- #
website_entry = Entry(font=("Segoe UI", 10), width=22)
website_entry.grid(row=1, column=1, sticky="w")
website_entry.focus()

email_entry = Entry(font=("Segoe UI", 10), width=38)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, "xyz@gmail.com")

password_entry = Entry(font=("Segoe UI", 10), width=22)
password_entry.grid(row=3, column=1, sticky="w")

# ---------------------------- BUTTONS ------------------------------- #
Button(
    text="Search",
    width=12,
    bg="#4CAF50",
    fg="white",
    command=search_password
).grid(row=1, column=2, padx=5)

Button(
    text="Generate",
    width=12,
    bg="#2196F3",
    fg="white",
    command=generate_password
).grid(row=3, column=2, padx=5)

eye_btn = Button(
    text="👁",
    width=3,
    command=toggle_password
)

eye_btn.grid(row=3, column=2, sticky="e", padx=(0, 90))

Button(
    text="📋",
    width=3,
    command=copy_password
).grid(row=3, column=2, sticky="e")

Button(
    text="Add Password",
    width=36,
    bg="#FF9800",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=save_password
).grid(row=4, column=1, columnspan=2, pady=15)

window.mainloop()
