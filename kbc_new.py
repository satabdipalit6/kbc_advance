import sqlite3
import random
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
import pymysql

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
        Button(self.centerframe, text="Continue", font=("Arial", 16), command=self.save_name_and_ask_difficulty).pack(pady=10)

    def save_name_and_ask_difficulty(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        self.ask_difficulty()

    def ask_difficulty(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Missing Info", "Please enter your name.")
            return
        self.clear_screen()
        Label(self.centerframe, text="Choose Difficulty Level", font=("Arial", 20), bg='black', fg='white').pack(pady=20)
        for level in ["Easy", "Medium", "Hard"]:
            Button(self.centerframe, text=level, font=("Arial", 16), width=15, command=lambda l=level: self.start_game(l)).pack(pady=10)

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
        self.gameframe = Frame(self.centerframe, bg='black')
        self.gameframe.pack(fill=BOTH, expand=True)

        # Question Label
        self.question_label = Label(self.root, text="", font=("Arial", 20, "bold"),bg='black', fg='white', wraplength=1200, justify=LEFT)
        self.question_label.pack(pady=30)

        # Frame for option buttons in grid layout
        self.options_frame = Frame(self.root, bg='black')
        self.options_frame.pack(pady=10)

        self.buttons = []
        for i in range(2):
            for j in range(2):
                btn = Button(self.options_frame, text="", font=('Arial', 18), width=30,
                             height=2, bg='gray20', fg='white',
                             command=lambda index=(i * 2 + j): self.check_answer(index))
                btn.grid(row=i, column=j, padx=10, pady=10)
                self.buttons.append(btn)

        # Timer
        self.timer_label = Label(self.root, text="Time Left: 30", font=("Arial", 16), bg='black', fg='yellow')
        self.timer_label.pack(pady=10)

        # Lifeline Buttons
        self.lifeline_frame = Frame(self.root, bg='black')
        self.lifeline_frame.pack(pady=10)

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
            database='questions'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz WHERE difficulty = %s", (difficulty,))
        all_questions = cursor.fetchall()
        conn.close()
        selected = random.sample(all_questions, min(15, len(all_questions)))
        return ([q[1] for q in selected], [q[2] for q in selected], [q[3] for q in selected],
                [q[4] for q in selected], [q[5] for q in selected], [q[6] for q in selected])

    def load_question(self):


        # Start the timer
        self.timer_running = True
        self.seconds_left = 30
        self.update_timer()
        # Display the question and options
        self.question_label.config(text=self.questions[self.q_index])
        options = [self.options1[self.q_index], self.options2[self.q_index],
                   self.options3[self.q_index], self.options4[self.q_index]]
        for i, btn in enumerate(self.buttons):
            btn.config(text=options[i], state=NORMAL)

            # Update prize image
        if self.q_index < len(self.prize_images):
            self.prizelbl.config(image=self.prize_images[self.q_index])
            self.prizelbl.image = self.prize_images[self.q_index]  # Prevent garbage collection

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
        selected = self.buttons[idx].cget("text").strip().lower()
        correct = self.correct_answers[self.q_index].strip().lower()

        if selected == correct:
            self.score += 10
            self.q_index += 1
            if self.q_index < len(self.questions):
                self.load_question()
            else:
                self.end_game()
        else:
            messagebox.showerror("Wrong Answer", "Oops! That was the wrong answer.")
            self.end_game()

    def use_5050(self):
        if self.used_5050: return
        self.used_5050 = True
        #mixer.music.play()
        correct = self.correct_answers[self.q_index]
        options = [self.options1[self.q_index], self.options2[self.q_index],
                   self.options3[self.q_index], self.options4[self.q_index]]

        # Find indices of incorrect options
        incorrect_indices = [i for i, opt in enumerate(options) if opt != correct]

        # Randomly pick 2 incorrect options to disable
        for i in random.sample(incorrect_indices, 2):
            self.buttons[i].config(text="", state=DISABLED, bg='black', activebackground='black', relief=FLAT, highlightthickness=0, borderwidth=0)




    def use_poll(self):
        if self.used_poll: return
        self.used_poll = True
        #messagebox.showinfo("Audience Poll", "Audience suggests option with most votes is likely correct.")
        self.show_audience_poll()

    def show_audience_poll(self):
        # Create a new window for the audience poll
        poll_window = Toplevel(self.root)
        poll_window.title("Audience Poll")
        poll_window.geometry("400x300")
        poll_window.configure(bg='black')


        # Schedule the poll window to close after 5 seconds (5000 milliseconds)
        poll_window.after(5000, poll_window.destroy)


        # Create a canvas to draw the bar chart
        canvas = Canvas(poll_window, width=400, height=300, bg='black', highlightthickness=0)
        canvas.pack()

        # Retrieve the current question's options and correct answer
        options = [
            self.options1[self.q_index],
            self.options2[self.q_index],
            self.options3[self.q_index],
            self.options4[self.q_index]
        ]
        correct_answer = self.correct_answers[self.q_index]

        # Determine the index of the correct answer
        correct_index = options.index(correct_answer)

        # Assign a higher percentage to the correct answer
        correct_percentage = random.randint(40, 70)
        remaining_percentage = 100 - correct_percentage

        # Distribute the remaining percentage among other options
        percentages = [0] * 4
        percentages[correct_index] = correct_percentage
        other_indices = [i for i in range(4) if i != correct_index]
        for i in other_indices[:-1]:
            val = random.randint(0, remaining_percentage)
            percentages[i] = val
            remaining_percentage -= val
        percentages[other_indices[-1]] = remaining_percentage

        # Define bar properties
        bar_width = 50
        spacing = 30
        max_height = 150
        x_start = 50
        option_labels = ['A', 'B', 'C', 'D']
        colors = ['red', 'green', 'blue', 'yellow']

        # Draw the bars and labels
        for i, percent in enumerate(percentages):
            bar_height = (percent / 100) * max_height
            x0 = x_start + i * (bar_width + spacing)
            y0 = 250 - bar_height
            x1 = x0 + bar_width
            y1 = 250

            # Draw the bar
            canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline='white')

            # Add the percentage label above the bar
            canvas.create_text((x0 + x1) / 2, y0 - 10, text=f"{percent}%", fill='white', font=('Arial', 12))

            # Add the option label below the bar
            canvas.create_text((x0 + x1) / 2, y1 + 10, text=option_labels[i], fill='white', font=('Arial', 12))



    def use_phone(self):
        if self.used_phone: return
        self.used_phone = True
        correct = self.correct_answers[self.q_index]
        messagebox.showinfo("Phone a Friend", f"Your friend thinks the correct answer might be: {correct}")

    def end_game(self):
        self.timer_running = False

        # Update prize image to final level
        if self.q_index < len(self.prize_images):
            self.prizelbl.config(image=self.prize_images[self.q_index])
            self.prizelbl.image = self.prize_images[self.q_index]  # Prevent garbage collection

        # Save game result to database
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='questions'
            )
            cursor = conn.cursor()

            # Ensure table exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS GameSession (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(100),
                    difficulty VARCHAR(50),
                    score INT,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insert the current game session
            cursor.execute(
                'INSERT INTO GameSession (player_name, difficulty, score) VALUES (%s, %s, %s)',
                (self.player_name, self.difficulty, self.score)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error saving game to DB:", e)

        # Clear the entire screen
        for widget in self.root.winfo_children():
            widget.destroy()

        #print("END GAME TRIGGERED")  # For debugging

        # Show final result
        Label(self.root, text=f"Game Over, {self.player_name}!", font=("Arial", 30), bg="black", fg="white").pack(pady=50)
        Label(self.root, text=f"Your Score: {self.score}", font=("Arial", 24), bg="black", fg="yellow").pack(pady=20)
        Button(self.root, text="Exit", font=("Arial", 18), command=self.root.quit).pack(pady=20)


    def clear_screen(self):
        for widget in self.centerframe.winfo_children():
            widget.destroy()
        if hasattr(self, 'gameframe'):
            self.gameframe.destroy()


def main():
    root = Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()


'''with open("/mnt/data/X.py", "w") as f:
        f.write(X.strip())'''