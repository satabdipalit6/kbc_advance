import sqlite3
import random
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
import pymysql.connector

class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("KBC Game")
        self.root.geometry("1520x900+0+0")
        self.root.config(bg='black')

        self.score = 0
        self.q_index = 0
        self.seconds_left = 30
        self.timer_running = False
        self.used_5050 = False
        self.used_poll = False
        self.used_phone = False
        self.player_name = ""
        self.difficulty = ""
        self.prize_images = [ImageTk.PhotoImage(file=f'Picture{i}.png') for i in range(15)]
        self.setup_ui()


    def setup_ui(self):
        self.topframe = Frame(self.root, bg='black')
        self.topframe.pack(side=TOP, fill=X)

        self.centerframe = Frame(self.root, bg='black')
        self.centerframe.pack(side=LEFT, fill=BOTH, expand=True)

        self.rightframe = Frame(self.root, bg='black')
        self.rightframe.pack(side=RIGHT, fill=Y)

        Label(self.topframe, text="Kaun Banega Crorepati", font=("Arial", 30, "bold"), bg='black', fg='yellow').pack(pady=20)

        self.centerImage = ImageTk.PhotoImage(file='center1.png')
        Label(self.centerframe, image=self.centerImage, bg='black').pack(pady=20)

        Button(self.centerframe, text="Start Game", font=('Arial', 20), bg='yellow', fg='black', command=self.ask_name).pack(pady=30)

        self.prizelbl = Label(self.rightframe, image=self.prize_images[0], bg='black')
        self.prizelbl.pack()

    def ask_name(self):
        self.clear_screen()
        Label(self.centerframe, text="Enter Your Name:", font=("Arial", 20), bg='black', fg='white').pack(pady=10)
        self.name_entry = Entry(self.centerframe, font=("Arial", 18))
        self.name_entry.pack(pady=10)
        Button(self.centerframe, text="Continue", font=("Arial", 16), command=self.ask_difficulty).pack(pady=10)

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
        self.questions, self.options1, self.options2, self.options3, self.options4, self.correct_answers = self.load_questions_from_db(
            difficulty)
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

        self.timer_label = Label(self.centerframe, text="Time Left: 30", font=("Arial", 16), bg='black', fg='yellow')
        self.timer_label.pack(pady=10)

        self.lifeline_5050_img = ImageTk.PhotoImage(file='50-50.png')
        self.lifeline_audience_img = ImageTk.PhotoImage(file='audiencePole.png')
        self.lifeline_phone_img = ImageTk.PhotoImage(file='phoneAFriend.png')

        Button(self.lifeline_frame, image=self.lifeline_5050_img, command=self.use_5050, bd=0, bg='black').grid(row=0,column=0,padx=10)
        Button(self.lifeline_frame, image=self.lifeline_audience_img, command=self.use_poll, bd=0, bg='black').grid(row=0, column=1, padx=10)
        Button(self.lifeline_frame, image=self.lifeline_phone_img, command=self.use_phone, bd=0, bg='black').grid(row=0,column=2,padx=10)

    def load_questions_from_db(self, difficulty):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='questions.db'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz WHERE difficulty = ?", (difficulty,))
        all_questions = cursor.fetchall()
        conn.close()
        selected = random.sample(all_questions, min(15, len(all_questions)))
        return ([q[1] for q in selected], [q[2] for q in selected], [q[3] for q in selected],
                [q[4] for q in selected], [q[5] for q in selected], [q[6] for q in selected])
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
def main():
    root = Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()