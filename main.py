import tkinter as tk
import pandas as pd
import time
import random

# ---------------------------- DATA ------------------------------- #


current_word = {}

try:
    data_file = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    data_file = pd.read_csv("data/french_words.csv")
    word_list = data_file.to_dict("records")

else:
    word_list = data_file.to_dict("records")

# ---------------------------- UI SETUP ------------------------------- #


def new_word():
    global current_word, flip
    window.after_cancel(flip)
    current_word = random.choice(word_list)
    f_word = current_word["French"]
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(french_word, text=f_word, fill="black")
    flip = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(french_word, text=current_word["English"], fill="white")
    canvas.itemconfig(card, image=card_back)


def is_known():
    word_list.remove(current_word)
    print(len(word_list))
    new_data = pd.DataFrame(word_list)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    new_word()


# ---------------------------- UI SETUP ------------------------------- #


# Window
window = tk.Tk()
window.resizable(False, False)
window.configure(padx=50, pady=50, bg="#B1DDC6")

flip = window.after(3000, func=flip_card)


# Window elements

# Card canvas
canvas = tk.Canvas(width=800, height=526)
canvas.config(bg="#B1DDC6", highlightthickness=0)
card_front = tk.PhotoImage(file="images/card_front.png")
card_back = tk.PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=wrong, bd=0, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)


right = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=right, bd=0, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

new_word()


window.mainloop()
