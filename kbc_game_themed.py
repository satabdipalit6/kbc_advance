# Create a simplified themed version of the KBC game using available assets


import sqlite3
import random
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer

class GameWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("KBC Game")
        self.root.geometry("1520x900+0+0")
        self.root.config(bg='black')

        #mixer.init()
       # mixer.music.load('50-50.mp3')  # preload example sound

        self.score = 0
        self.seconds_left = 30
        self.timer_running = False
        self.used_5050 = False
        self.used_poll = False
        self.used_friend = False
        self.player_name = ""
        self.difficulty = ""

        self.setup_ui()

    def setup_ui(self):
        # Top Frame (Header)
        topframe = Frame(self.root, bg='green', height=100)
        topframe.pack(fill=X)
        Label(topframe, text="KBC - Themed Quiz Game", font=("Arial", 28, "bold"), bg='yellow').pack(pady=20)

        # Center Logo
        self.logo_img = ImageTk.PhotoImage(file='center.png')
        logo_lbl = Label(self.root, image=self.logo_img, bg='black')
        logo_lbl.pack(pady=10)

        # Start Button
        Button(self.root, text="Start Game", font=('Arial', 18), bg='yellow', fg='black',
               command=self.ask_name).pack(pady=20)

    def ask_name(self):
        self.clear_screen()
        Label(self.root, text="Enter Your Name:", font=("Arial", 20), bg='black', fg='white').pack(pady=10)
        self.name_entry = Entry(self.root, font=("Arial", 18))
        self.name_entry.pack(pady=10)
        Button(self.root, text="Continue", font=("Arial", 16), command=self.ask_difficulty).pack(pady=10)

    def ask_difficulty(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Missing Info", "Please enter your name.")
            return
        self.clear_screen()
        Label(self.root, text="Choose Difficulty Level", font=("Arial", 20), bg='black', fg='white').pack(pady=20)
        for level in ["Easy", "Medium", "Hard"]:
            Button(self.root, text=level, font=("Arial", 16), width=15, command=lambda l=level: self.start_game(l)).pack(pady=10)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.questions, self.options1, self.options2, self.options3, self.options4, self.correct_answers = self.load_questions_from_db(difficulty)
        self.q_index = 0
        self.score = 0
        self.clear_screen()
        self.setup_game_ui()
        self.load_question()

    def setup_game_ui(self):
        self.question_label = Label(self.root, text="", font=("Arial", 20, "bold"), bg='black', fg='white', wraplength=1200, justify=LEFT)
        self.question_label.pack(pady=30)

        self.buttons = []
        for i in range(4):
            btn = Button(self.root, text="", font=('Arial', 18), width=50, bg='gray20', fg='white', command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Lifeline Buttons
        lifeline_frame = Frame(self.root, bg='black')
        lifeline_frame.pack(pady=20)

        self.lifeline_5050_img = ImageTk.PhotoImage(file='50-50.png')
        self.lifeline_audience_img = ImageTk.PhotoImage(file='audiencePole.png')
        self.lifeline_audienceX_img = ImageTk.PhotoImage(file='audiencePoleX.png')

        Button(lifeline_frame, image=self.lifeline_5050_img, command=self.use_5050, bd=0, bg='black').grid(row=0, column=0, padx=10)
        Button(lifeline_frame, image=self.lifeline_audience_img, command=self.use_poll, bd=0, bg='black').grid(row=0, column=1, padx=10)

        self.timer_label = Label(self.root, text="Time Left: 30", font=("Arial", 16), bg='black', fg='yellow')
        self.timer_label.pack()

    def load_questions_from_db(self, difficulty):
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz WHERE difficulty = ?", (difficulty,))
        all_questions = cursor.fetchall()
        conn.close()
        selected = random.sample(all_questions, min(15, len(all_questions)))
        return ([q[1] for q in selected], [q[2] for q in selected], [q[3] for q in selected],
                [q[4] for q in selected], [q[5] for q in selected], [q[6] for q in selected])

    def load_question(self):
        self.timer_running = True
        self.seconds_left = 30
        self.update_timer()
        self.question_label.config(text=self.questions[self.q_index])
        options = [self.options1[self.q_index], self.options2[self.q_index],
                   self.options3[self.q_index], self.options4[self.q_index]]
        for i, btn in enumerate(self.buttons):
            btn.config(text=options[i], state=NORMAL)

    def update_timer(self):
        if self.timer_running and self.seconds_left > 0:
            self.timer_label.config(text=f"Time Left: {self.seconds_left}")
            self.seconds_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.seconds_left == 0:
            self.timer_running = False
            messagebox.showinfo("Time's up", "You ran out of time!")
            self.end_game()

    def check_answer(self, idx):
        self.timer_running = False
        if self.buttons[idx].cget("text") == self.correct_answers[self.q_index]:
            self.score += 10
            self.q_index += 1
            if self.q_index < len(self.questions):
                self.load_question()
            else:
                self.end_game()
        else:
            self.end_game()

    def use_5050(self):
        if self.used_5050: return
        self.used_5050 = True
        mixer.music.play()
        correct = self.correct_answers[self.q_index]
        options = [self.options1[self.q_index], self.options2[self.q_index],
                   self.options3[self.q_index], self.options4[self.q_index]]
        incorrect_indices = [i for i, opt in enumerate(options) if opt != correct]
        for i in random.sample(incorrect_indices, 2):
            self.buttons[i].config(state=DISABLED)

    def use_poll(self):
        if self.used_poll: return
        self.used_poll = True
        messagebox.showinfo("Audience Poll", "Audience suggests option with most votes is likely correct.")

    def end_game(self):
        self.clear_screen()
        Label(self.root, text=f"Thank you {self.player_name}! Your Score: {self.score}", font=("Arial", 24), bg='black', fg='white').pack(pady=30)
        Button(self.root, text="Exit", font=("Arial", 16), command=self.root.quit).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# Save to file
with open("/mnt/data/kbc_game_themed.py", "w") as f:
    f.write(kbc_game_themed.strip())
