import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import requests
import random
import html

GENRE_CATEGORIES = {
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Science & Nature": 17,
    "Computers": 18,
    "Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28
}


class QuestionEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Question Entry")
        self.root.geometry("950x650")
        self.root.configure(bg="#1c1c1c")
        self.root.minsize(800, 500)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Background Gradient (Black to Lavender)
        self.root.tk_setPalette(background="#1c1c1c", foreground="#ffffff")

        # General styling for labels (no background)
        self.style.configure("TLabel", foreground="black", font=("Segoe UI", 12, "bold"))

        # Entry styling with rounded corners and shadow effect
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 12), relief="flat", borderwidth=2)

        # Button Styling with Hover Effect and Rounded Corners
        self.style.configure("TButton", background="#8e44ad", foreground="white", font=("Segoe UI", 12, "bold"),
                             padding=8, relief="flat", width=20)
        self.style.map("TButton",
                       background=[('active', '#9b59b6')],
                       foreground=[('active', 'white')])

        # Combobox (Genre, Difficulty) Styling
        self.style.configure("TCombobox", font=("Segoe UI", 12), padding=6)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        labels = ['Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Option', 'Difficulty', 'Genre']
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = ttk.Label(main_frame, text=label + ":", anchor="w")
            lbl.grid(row=i, column=0, sticky="w", padx=15, pady=12)

            if label == 'Difficulty':
                self.difficulty_var = tk.StringVar()
                cb = ttk.Combobox(main_frame, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"],
                                  state="readonly", width=50)
                cb.grid(row=i, column=1, sticky="ew", padx=10, pady=12)
                self.entries[label] = cb
            elif label == 'Genre':
                self.genre_var = tk.StringVar()
                cb = ttk.Combobox(main_frame, textvariable=self.genre_var, values=list(GENRE_CATEGORIES.keys()),
                                  state="readonly", width=50)
                cb.grid(row=i, column=1, sticky="ew", padx=10, pady=12)
                cb.set("General Knowledge")
                self.entries[label] = cb
            else:
                entry = ttk.Entry(main_frame, width=50)
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=12)
                self.entries[label] = entry

        for i in range(len(labels)):
            main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Buttons with Hover Effects
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=30)

        fetch_btn = ttk.Button(button_frame, text="🌐 Fetch From Internet", command=self.fetch_question)
        fetch_btn.grid(row=0, column=0, padx=25)

        submit_btn = ttk.Button(button_frame, text="💾 Submit to Database", command=self.submit_to_db)
        submit_btn.grid(row=0, column=1, padx=25)

    def fetch_question(self):
        try:
            genre = self.entries['Genre'].get()
            category_id = GENRE_CATEGORIES.get(genre, 9)

            response = requests.get(
                f"https://opentdb.com/api.php?amount=1&category={category_id}&type=multiple"
            )
            data = response.json()
            if data["response_code"] == 0:
                result = data["results"][0]

                # Decode the HTML entities
                question = html.unescape(result['question'])
                self.entries['Question'].delete(0, tk.END)
                self.entries['Question'].insert(0, question)

                options = [html.unescape(opt) for opt in result['incorrect_answers']] + [
                    html.unescape(result['correct_answer'])]
                random.shuffle(options)

                for i, opt in enumerate(['Option A', 'Option B', 'Option C', 'Option D']):
                    self.entries[opt].delete(0, tk.END)
                    self.entries[opt].insert(0, options[i])

                correct_option = html.unescape(result['correct_answer'])
                self.entries['Correct Option'].delete(0, tk.END)
                self.entries['Correct Option'].insert(0, correct_option)

                diff = result['difficulty'].capitalize()
                self.difficulty_var.set(diff if diff in ['Easy', 'Medium', 'Hard'] else 'Medium')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch question: {e}")

    def submit_to_db(self):
        try:
            q_data = {
                'question': self.entries['Question'].get().strip(),
                'optionA': self.entries['Option A'].get().strip(),
                'optionB': self.entries['Option B'].get().strip(),
                'optionC': self.entries['Option C'].get().strip(),
                'optionD': self.entries['Option D'].get().strip(),
                'correctOption': self.entries['Correct Option'].get().strip(),
                'difficulty': self.entries['Difficulty'].get().strip().lower()
            }

            if not all(q_data.values()):
                messagebox.showwarning("Incomplete", "Please fill all fields.")
                return

            conn = pymysql.connect(host='localhost', user='root', password='root', database='questions')
            cursor = conn.cursor()

            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS quiz (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question VARCHAR(255) UNIQUE,
                    optionA TEXT,
                    optionB TEXT,
                    optionC TEXT,
                    optionD TEXT,
                    correctOption TEXT,
                    difficulty VARCHAR(10)
                );
            ''')

            cursor.execute('''
                INSERT INTO quiz (question, optionA, optionB, optionC, optionD, correctOption, difficulty)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (q_data['question'], q_data['optionA'], q_data['optionB'],
                  q_data['optionC'], q_data['optionD'], q_data['correctOption'], q_data['difficulty']))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question submitted successfully.")
        except pymysql.err.IntegrityError:
            messagebox.showerror("Duplicate", "This question already exists in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")


def main():
    root = tk.Tk()
    app = QuestionEntryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
