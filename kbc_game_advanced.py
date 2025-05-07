# Generate a new version of the advanced KBC game with all features integrated.


import sqlite3
import random
import time
import threading
from tkinter import *
from tkinter import messagebox

class GameWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("KBC Game")
        self.root.geometry("1000x650")
        self.root.config(bg='black')

        self.score = 0
        self.high_score_file = "high_scores.txt"
        self.used_5050 = False
        self.used_poll = False
        self.used_friend = False
        self.timer_running = True
        self.seconds_left = 30
        self.difficulty = None

        self.setup_start_screen()

    def setup_start_screen(self):
        self.clear_screen()
        title = Label(self.root, text="🎮 Welcome to KBC Game!", font=("Arial", 24, "bold"), fg="white", bg="black")
        title.pack(pady=20)

        Label(self.root, text="Select Difficulty:", font=("Arial", 16), fg="white", bg="black").pack(pady=10)
        for level in ["Easy", "Medium", "Hard"]:
            Button(self.root, text=level, font=("Arial", 14), width=20, command=lambda l=level: self.start_game(l)).pack(pady=5)

    def start_game(self, difficulty_level):
        self.difficulty = difficulty_level
        self.questions, self.options1, self.options2, self.options3, self.options4, self.correct_answers = self.load_questions_from_db(difficulty_level)
        self.q_index = 0
        self.score = 0
        self.used_5050 = self.used_poll = self.used_friend = False
        self.clear_screen()
        self.build_question_ui()
        self.load_question()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_question_ui(self):
        self.question_label = Label(self.root, text="", font=('arial', 16, 'bold'), fg='white', bg='black', wraplength=900, justify='left')
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = Button(self.root, text="", font=('arial', 14), bg='gray20', fg='white', width=40, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.lifeline_frame = Frame(self.root, bg='black')
        self.lifeline_frame.pack(pady=10)
        Button(self.lifeline_frame, text="50:50", command=self.use_5050).grid(row=0, column=0, padx=10)
        Button(self.lifeline_frame, text="Audience Poll", command=self.use_poll).grid(row=0, column=1, padx=10)
        Button(self.lifeline_frame, text="Phone a Friend", command=self.use_friend).grid(row=0, column=2, padx=10)

        self.timer_label = Label(self.root, text="Time left: 30", font=("Arial", 14), fg="yellow", bg="black")
        self.timer_label.pack(pady=10)

    def load_questions_from_db(self, difficulty):
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz WHERE difficulty = ?", (difficulty,))
        all_questions = cursor.fetchall()
        conn.close()

        selected = random.sample(all_questions, min(15, len(all_questions)))
        questions = [q[1] for q in selected]
        options1 = [q[2] for q in selected]
        options2 = [q[3] for q in selected]
        options3 = [q[4] for q in selected]
        options4 = [q[5] for q in selected]
        correct = [q[6] for q in selected]
        return questions, options1, options2, options3, options4, correct

    def load_question(self):
        self.timer_running = True
        self.seconds_left = 30
        self.update_timer()

        self.question_label.config(text=self.questions[self.q_index])
        opts = [self.options1[self.q_index], self.options2[self.q_index], self.options3[self.q_index], self.options4[self.q_index]]
        for i, btn in enumerate(self.buttons):
            btn.config(text=opts[i], state=NORMAL)

    def update_timer(self):
        if self.seconds_left > 0 and self.timer_running:
            self.timer_label.config(text=f"Time left: {self.seconds_left}")
            self.seconds_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.seconds_left == 0:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.end_game()

    def check_answer(self, selected_index):
        self.timer_running = False
        selected_text = self.buttons[selected_index].cget('text')
        correct = self.correct_answers[self.q_index]
        if selected_text == correct:
            self.score += 10
            self.q_index += 1
            if self.q_index < len(self.questions):
                self.load_question()
            else:
                self.end_game()
        else:
            self.end_game()

    def use_5050(self):
        if self.used_5050:
            return
        self.used_5050 = True
        correct = self.correct_answers[self.q_index]
        options = [self.options1[self.q_index], self.options2[self.q_index], self.options3[self.q_index], self.options4[self.q_index]]
        indices = [i for i, opt in enumerate(options) if opt != correct]
        to_remove = random.sample(indices, 2)
        for i in to_remove:
            self.buttons[i].config(state=DISABLED)

    def use_poll(self):
        if self.used_poll:
            return
        self.used_poll = True
        # Fake percentages with higher chance for correct answer
        percentages = [random.randint(10, 30) for _ in range(4)]
        correct_index = [self.options1, self.options2, self.options3, self.options4].index(
            [lst for lst in [self.options1, self.options2, self.options3, self.options4] if self.correct_answers[self.q_index] in lst][0])
        percentages[correct_index] += 40
        messagebox.showinfo("Audience Poll", f"Poll Results:\nA: {percentages[0]}%\nB: {percentages[1]}%\nC: {percentages[2]}%\nD: {percentages[3]}%")

    def use_friend(self):
        if self.used_friend:
            return
        self.used_friend = True
        messagebox.showinfo("Phone a Friend", f"Your friend thinks the answer is: {self.correct_answers[self.q_index]}")

    def end_game(self):
        self.timer_running = False
        self.update_high_score()
        self.clear_screen()
        msg = f"Game Over! Your Score: {self.score}"
        Label(self.root, text=msg, font=('Arial', 20, 'bold'), fg='white', bg='black').pack(pady=30)
        self.show_high_scores()
        Button(self.root, text="Play Again", command=self.setup_start_screen, font=('Arial', 14)).pack(pady=10)
        Button(self.root, text="Exit", command=self.root.quit, font=('Arial', 14)).pack()

    def update_high_score(self):
        name = "Player"
        try:
            with open(self.high_score_file, "a") as f:
                f.write(f"{name},{self.score}\\n")
        except:
            pass

    def show_high_scores(self):
        Label(self.root, text="🏆 High Scores:", font=('Arial', 16, 'bold'), fg='yellow', bg='black').pack()
        try:
            with open(self.high_score_file, "r") as f:
                scores = [line.strip().split(",") for line in f.readlines()]
                scores.sort(key=lambda x: int(x[1]), reverse=True)
                for i, (name, score) in enumerate(scores[:5]):
                    Label(self.root, text=f"{i+1}. {name}: {score}", font=('Arial', 14), fg='white', bg='black').pack()
        except:
            Label(self.root, text="No scores available yet.", font=('Arial', 14), fg='white', bg='black').pack()

def main():
    root = Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# Save the advanced game file
with open("/mnt/data/kbc_game_advanced.py", "w") as f:
    f.write(kbc_game_advanced.strip())
