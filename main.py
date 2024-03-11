from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # create lists of random letters, symbols, and numbers
    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    # generate a random password from the three lists
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    generated_password = "".join(password_list)
    password_entry.insert(0, generated_password)

    # copy the generated password
    pyperclip.copy(generated_password)


def save():
    # this function adds website, email, and password to
    # json file when the user hits the "add" button

    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # if any of the entries are blank, throw a warning
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning!", message="Please don't leave any fields empty!")
    # handle adding and updating data to .json file
    else:
        try:
            # try opening json file in read mode
            with open("password-manager.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            # if FileNotFoundError is thrown, create a json
            # file and add the new data to it
            with open("password-manager.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # update old data then add it to the file if file
            # was opened in read mode successfully
            data.update(new_data)

            with open("password-manager.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            # clear website and password entries
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    # this function looks for email and password of a website
    # from json file and displays it in a popup window based
    # on the website the user chooses to search for
    website = website_entry.get()
    try:
        # open json file in read mode
        with open("password-manager.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # if theres a FileNotFoundError error, handle it with a popup box
        messagebox.showerror(title="Error!", message="File not found.")
    else:
        # if the website the user is looking for is found in file,
        # get the credentials to logging in and display it in a popup box
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No information for {website} was found")


# create password manager window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# create canvas and add the logo
canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(column=1, row=0)

# create the website, email/username, and password labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# create the website, email/username, and password entries
website_entry = Entry(width=45)
website_entry.grid(column=1, row=1)

email_username_entry = Entry(width=45)
email_username_entry.grid(column=1, row=2)
email_username_entry.insert(0, "m.rocha@gmail.com")

password_entry = Entry(width=45)
password_entry.grid(column=1, row=3)

# add search, generate password, and add buttons
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4)

window.mainloop()