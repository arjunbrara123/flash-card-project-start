from tkinter import *
import pandas
import random
import json

BACKGROUND_COLOR = "#B1DDC6"

# Read in language flashcard data
try:
    with open("words_to_learn.csv") as file:
        dWords = json.load(file)
except FileNotFoundError:
    with open("data/french_words.csv") as file:
        data = pandas.read_csv(file)
        dWords = dict(zip(data.French, data.English))

# Create card functionality
flip_timer = None
new_word = None
dWrong = dict()
dRight = dict()

def word_no():
    dWrong[new_word] = dWords[new_word]
    print(dWrong)
    with open("words_to_learn.csv", "w") as file:
        json.dump(dWrong, file, indent=4)
    next_card()


def word_yes():
    dRight[new_word] = dWords[new_word]
    try:
        del dWrong[new_word]
    except KeyError:
        del dWords[new_word]
    print(dRight)
    next_card()


def next_card():
    #global tk_card
    global new_word, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    new_word = random.choice(list(dWords.keys()))
    canvas.itemconfig(imgCard, image=imgFront)
    canvas.itemconfig(lblTitle, text="French", fill="black")
    canvas.itemconfig(lblWord, text=new_word, fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    print(dWords)
    translated_word = dWords[new_word]
    canvas.itemconfig(lblTitle, text="English", fill="white")
    canvas.itemconfig(imgCard, image=imgBack)
    canvas.itemconfig(lblWord, text=translated_word, fill="white")


# Set up initial GUI window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
new_word = random.choice(list(dWords.keys()))
window.after(3000, flip_card)

# Create middle card canvas
imgBack = PhotoImage(file="images/card_back.png")
imgFront = PhotoImage(file="images/card_front.png")
canvas = Canvas()
canvas.config(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
imgCard = canvas.create_image(400, 263, image=imgFront)
lblTitle = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
lblWord = canvas.create_text(400, 263, text=new_word, font=("Arial", 60, "italic"))
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

# Create buttons at the bottom
imgNo = PhotoImage(file="images/wrong.png")
imgYes = PhotoImage(file="images/right.png")

btnNo = Button(image=imgNo, command=word_no).grid(column=0, row=2)
btnYes = Button(image=imgYes, command=word_yes).grid(column=1, row=2)

# Initialise
window.mainloop()

# Show random card
next_card()
