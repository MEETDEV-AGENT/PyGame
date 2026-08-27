import tkinter as tk
from tkinter import messagebox
import requests

# --- Quiz Database ---#
def fetch_questions():
    """Fetch questions from OpenTDB API"""
    try:
        response = requests.get(url = "https://opentdb.com/api.php?amount=50&difficulty=hard&type=boolean")
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except:
        return []

# --- Quiz Logic Class ---#
class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_q = self.question_list[self.question_number]
        self.question_number += 1
        q_text = current_q["question"]
        q_text = (q_text
            .replace("&quot;", '"')
            .replace("&apos;", "'")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">"))
        return q_text

    def check_answer(self, user_answer):
        correct_answer = self.question_list[self.question_number - 1]["correct_answer"]
        correct_answer = (correct_answer
            .replace("&quot;", '"')
            .replace("&apos;", "'")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">"))
    
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
    
    def reset_quiz(self):
        """Reset quiz state for restart"""
        self.question_number = 0
        self.score = 0

# --- Quiz UI Class ---#
class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg="#375362")

        self.score_label = tk.Label(text="Score: 0", fg="white", bg="#375362", font=("Arial", 14, "bold"))
        self.score_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125, width=280, text="Loading...", fill="#375362", font=("Arial", 16, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.true_button = tk.Button(text="✔️", font=("Arial", 20), width=5, bg="green", fg="white", command=self.true_pressed)
        self.true_button.grid(row=2, column=0)

        self.false_button = tk.Button(text="❌", font=("Arial", 20), width=5, bg="red", fg="white", command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.restart_button = tk.Button(text="🔄 Restart", font=("Arial", 12), width=10, bg="#375362", fg="white", command=self.restart_quiz)
        self.restart_button.grid(row=3, column=0, columnspan=2, pady=20)
        self.restart_button.config(state="disabled")  

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.restart_button.config(state="disabled")  
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
            self.canvas.itemconfig(self.question_text, text="🎉 Quiz Complete!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.restart_button.config(state="normal")  
            messagebox.showinfo("Quiz Completed", f"Your final score: {self.quiz.score}/{len(self.quiz.question_list)}")

# --- Starting new quiz ---#
    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="light green")
        else:
            self.canvas.config(bg="salmon")
        self.window.after(1000, self.get_next_question)
    
    def restart_quiz(self):
        """Restart the quiz with new questions"""
        # ✅ Fetch new questions from API
        new_questions = fetch_questions()
        
        if new_questions:
            # ✅ Reset quiz brain with new questions
            self.quiz.question_list = new_questions
            self.quiz.reset_quiz()
            
            # ✅ Reset UI
            self.score_label.config(text="Score: 0")
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
            self.restart_button.config(state="disabled")
            
            # ✅ Start fresh
            self.get_next_question()
        else:
            messagebox.showerror("Error", "Failed to load new questions. Check your internet connection.")

# --- Main Code ---#
question_data = fetch_questions()

if question_data:
    quiz = QuizBrain(question_data)
    quiz_ui = QuizInterface(quiz)
else:
    print("⚠️ No questions loaded. Check internet or try again later.")
