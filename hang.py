import random
import sqlite3
from tkinter import *
from tkinter import messagebox
from prettytable import PrettyTable


def database():
    conn = sqlite3.connect("hangman.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS hall_of_fame (
                      level TEXT,
                      winner_name TEXT,
                      remaining_lives INTEGER)''')
    conn.commit()
    conn.close()


def hall_of_fame(level, player_name, remaining_lives):
    conn = sqlite3.connect("hangman.db")
    cursor = conn.cursor()
    cursor.execute("Select remaining_lives FROM hall_of_fame WHERE level = ?", (level,))
    row = cursor.fetchone()

    if row is None or remaining_lives > row[0]:
        cursor.execute("REPLACE INTO hall_of_fame (level, winner_name, remaining_lives) VALUES (?, ?, ?)",
                       (level, player_name, remaining_lives))
        conn.commit()
    conn.close()


def hall_of_fame():
    conn = sqlite3.connect("hangman.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hall_of_fame")
    rows = cursor.fetchall()
    conn.close()

    table = PrettyTable(["Level", "Winner Name", "Remaining Lives"])
    for row in rows:
        table.add_row(row)
    messagebox.showinfo("Hall of Fame", table.get_string())


def word():
    global ss, ll, ss1, n, temps, selected_level
    word_sets = {
        "Animals": ["dog","elephant","zebra","ant", "baboon", "badger", "bat", "bear", "beaver", "camel", "cat", "clam", "cobra"],
        "Shapes": ["square","line","point", "triangle", "rectangle", "circle", "ellipse", "rhombus", "trapezoid"],
        "Places": ["Cairo","agra","mathura","noida","lucknow", "London", "Paris", "Baghdad", "Istanbul", "Riyadh"]
    }

    if selected_level.get() == "Easy" or selected_level.get() == "Moderate":
        chosen_set = category_var.get()
    else:
        chosen_set = random.choice(list(word_sets.keys()))

    ss = random.choice(word_sets[chosen_set])
    ll = ["*" for _ in ss]
    ss1 = len(ss)
    n = 8 if selected_level.get() == "Easy" else 6
    temps = ss
    leftchances.configure(text=f'Left = {n}')
    wordlabel.configure(text=' '.join(ll))
    ans.configure(text='')


def hangman():
    global ss, ll, ss1, n, temps
    first = inpp.get()
    input1.delete(0, END)
    if n > 0:
        if first in ss:
            for i in range(ss1):
                if ss[i] == first and ll[i] == '*':
                    ll[i] = ss[i]
                    ss = list(ss)
                    ss[i] = "*"
                    wordlabel.configure(text=' '.join(ll))
                    if ''.join(ll) == temps:
                        ans.configure(text='Congratulations! You won the game.')
                        hall_of_fame(selected_level.get(), player_name.get(), n)
                        res = messagebox.askyesno("Notification",
                                                  'Congratulations! You won the game.\nWant to play again?')
                        if res:
                            word()
                        else:
                            root.destroy()
                    break
        else:
            n -= 1
            leftchances.configure(text=f'Left = {n}')
    if n <= 0:
        ans.configure(text='You lost the game.')
        res = messagebox.askyesno("Notification", 'You lost the game.\nWant to play again?')
        if res:
            word()
        else:
            root.destroy()


def jj(event):
    hangman()


root = Tk()
root.geometry('800x600+300+100')
root.configure(bg='aquamarine')
root.title('Hangman Game')

Label(root, text='Enter Your Name:', font=('arial', 15, 'bold'), bg='cyan').place(x=50, y=20)
player_name = Entry(root, font=('arial', 15, 'bold'))
player_name.place(x=250, y=20)

Label(root, text='Select Difficulty:', font=('arial', 15, 'bold'), bg='cyan').place(x=50, y=60)
selected_level = StringVar(value='Easy')
OptionMenu(root, selected_level, "Easy", "Moderate", "Hard").place(x=250, y=60)

Label(root, text='Select Category:', font=('arial', 15, 'bold'), bg='cyan').place(x=50, y=100)
category_var = StringVar(value='Animals')
OptionMenu(root, category_var, "Animals", "Shapes", "Places").place(x=250, y=100)

Button(root, text='Start Game', font=('arial', 15, 'bold'), command=word).place(x=100, y=150)
Button(root, text='Hall of Fame', font=('arial', 15, 'bold'), command=hall_of_fame).place(x=250, y=150)

wordlabel = Label(root, text='', font=('arial', 35, 'bold'), bg='cyan')
wordlabel.place(x=300, y=200)

leftchances = Label(root, text='', font=('arial', 20, 'bold'), bg='cyan')
leftchances.place(x=600, y=100)

ans = Label(root, text='', font=('arial', 20, 'bold'), bg='cyan')
ans.place(x=100, y=500)

inpp = StringVar()
input1 = Entry(root, font=('arial', 20, 'bold'), relief=RIDGE, bd=5, bg='green', justify='center', fg='white',
               textvariable=inpp)
input1.focus_set()
input1.place(x=250, y=350)

Button(root, text='Submit', font=('arial', 15, 'bold'), width=15, bd=5, bg='red', activebackground='blue',
       activeforeground='white', command=hangman).place(x=300, y=400)
root.bind("<Return>", jj)

database()
root.mainloop()
