import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import json

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
SYMBOLS = "!@#%&()?*+$"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letter_freq = random.randint(8, 12)
    num_freq = random.randint(4, 6)
    symbol_freq = random.randint(4, 6)
    letter = random.sample(LETTERS, letter_freq)
    num = random.sample(NUMBERS, num_freq)
    symb = random.sample(SYMBOLS, symbol_freq)
    pswrd = letter + num + symb
    random.shuffle(pswrd)
    pswrd = "".join(pswrd)
    password.delete(0, END)
    password.insert(END, pswrd)
    pyperclip.copy(pswrd)


def check_blank_box():
    if website.get().strip() == "" or password.get().strip() == "" or mail_id.get().strip() == "":
        messagebox.showerror(title="Oops!!!!", message="All boxes must be filled!")
        return True


def check_password():
    for char in password.get().strip():
        if char not in LETTERS + NUMBERS + SYMBOLS:
            messagebox.showerror(title="Oops!!", message="The password is invalid!")
            return True


def check_presence():
    with open("password_data.json") as file:
        data = json.load(file)
        if website.get().strip() in data.keys():
            if data[website.get().strip()]["e-mail"] == mail_id.get():
                return "Do you want to change the saved password to this?"
        return "Do you want to save it?"


# ----------------------------- SEARCH WEBSITE-----------------------------------#
def search():
    if website.get().strip() == "":
        return
    try:
        with open("password_data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Alas!", message="No data file exists.")
    else:
        if website.get().strip() in data.keys():
            messagebox.showinfo(title=website.get(), message=f"E-mail: {data[website.get().strip()]['e-mail']}\n"
                                                             f"Password: {data[website.get().strip()]['password']}")
        else:
            messagebox.showinfo(title="Not Found", message="No details for the website exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    if check_blank_box() or check_password():
        return
    confirmation = messagebox.askokcancel(title=website.get().strip(), message=f"The details given-\n"
                                                                               f"E-mail:{mail_id.get().strip()}\n"
                                                                               f"Password:{password.get().strip()}\n"
                                                                               f"{check_presence()}")
    if confirmation:
        new_data = {website.get().strip(): {"e-mail": mail_id.get().strip(), "password": password.get().strip()}}
        try:
            with open("password_data.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("password_data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("password_data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            website.delete(0, END)
            password.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.geometry("500x400+500+200")
window.resizable(False, False)
window.config(padx=50)

canvas = Canvas(width=200, height=190)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 90, image=logo)
canvas.grid(column=0, columnspan=2, row=0)

website_label = Label(text="Website:", font=("Ariel", 16, "normal"))
website_label.grid(column=0, row=1, sticky="w")

website = Entry(width=30)
website.grid(column=1, row=1, sticky="w")

search_button = Button(text="Search", width=7, bg="gray", fg="white", command=search)
search_button.grid(column=1, row=1, sticky="e")

mail_id_label = Label(text="E-mail:", font=("Ariel", 16, "normal"))
mail_id_label.grid(column=0, row=2, sticky="w")

mail_id = Entry(width=40)
mail_id.insert(END, "anupamkumarpaul2005@gmail.com")
mail_id.grid(column=1, row=2)

password_label = Label(text="Password:", font=("Ariel", 16, "normal"))
password_label.grid(column=0, row=3, sticky="w")

password = Entry(width=30)
password.grid(column=1, row=3, sticky="w")

generate_password_button = Button(text="Generate", bg="gray", fg="white", command=generate_password)
generate_password_button.grid(column=1, row=3, sticky="e")

add_button = Button(text="Add", width=34, bg="gray", fg="white", command=add)
add_button.grid(column=1, row=4)

window.mainloop()
