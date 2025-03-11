import sqlite3
from tkinter import *
from functools import partial
from Levels import *

# Connect to the database
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, name TEXT, password TEXT, level INT)")

def main_login_page():
    # Create the main login window
    root = Tk()
    root.geometry('300x400')
    root.configure(background="white")
    root.title("Cannon Game - Login")

    # Login UI Elements
    header_Login = Label(root, text="Login", bg="green", fg="white", width=300, font="bold")
    header_Login.pack()

    alert_banner_Login = Label(root, text="", bg="white", fg="red", width=300, font="bold")
    alert_banner_Login.pack()

    username = StringVar()
    usernameLabel_Login = Label(root, text="Username *", bg="white", fg="green")
    usernameLabel_Login.place(x=20, y=40)
    usernameEntry_Login = Entry(root, textvariable=username, bg="white", fg="green", insertbackground="green")
    usernameEntry_Login.place(x=100, y=42)

    password = StringVar()
    passwordLabel_Login = Label(root, text="Password *", bg="white", fg="green")
    passwordLabel_Login.place(x=20, y=80)
    passwordEntry_Login = Entry(root, textvariable=password, show='*', bg="white", fg="green", insertbackground="green")
    passwordEntry_Login.place(x=100, y=82)

    def user_credential_Login():
        uname = username.get()
        pword = password.get()

        if len(uname) and len(pword) > 0:
            cursor.execute("SELECT password FROM Users WHERE username = ?", (uname,))
            result = cursor.fetchone()

            if result and pword == result[0]:
                alert_banner_Login.config(text="")
                print("******* Login *******")
                print("Username entered:", uname)
                print("Password entered:", pword)
                root.destroy()  # Destroy the login window
                level_page(uname)  # Proceed to level selection
            else:
                alert_banner_Login.config(text="Wrong username or password")
        else:
            alert_banner_Login.config(text="Fill in the required fields!")

    # Login Button
    loginButton_Login = Button(root, text="Login", width=8, height=1, bg="white", fg="green",
                               command=user_credential_Login)
    loginButton_Login.place(x=100, y=130)

    # Sign-up Button
    signUpButton_Login = Button(root, text="Sign up", width=5, height=1, bg="white", fg="green",
                                command=lambda: sign_up_page(root))
    signUpButton_Login.place(x=210, y=130)

    root.mainloop()

def sign_up_page(parent):
    # Create a separate Toplevel window for sign-up
    signup_window = Toplevel(parent)
    signup_window.geometry('300x400')
    signup_window.configure(background="white")
    signup_window.title("Cannon Game - Sign up")

    def go_back_to_login():
        signup_window.destroy()

    def sign_up_successful():
        # Clear the sign-up window and show a confirmation message
        for widget in signup_window.winfo_children():
            widget.destroy()
        header_sign_up = Label(signup_window, text="Sign up successful", bg="green", fg="white", width=300, font="bold")
        header_sign_up.pack()
        lable_sign_up_successful = Label(signup_window, text="You have successfully signed up\n\nYou can now sign in with your new account.", bg="white", fg="green")
        lable_sign_up_successful.pack()
        confirm_button_sign_up = Button(signup_window, text="Back to Login", width=8, height=1, bg="white", fg="green", command=go_back_to_login)
        confirm_button_sign_up.pack()

    def check_if_user_exist(username_val):
        cursor.execute("SELECT * FROM Users WHERE username == ?", (username_val,))
        found = cursor.fetchall()
        return len(found) == 1

    def user_credential_sign_up():
        name_val = name_var.get()
        username_val = username_var.get()
        password_val = password_var.get()
        level_val = 1  # Default starting level

        error = False
        if len(name_val) <= 2:
            alert_banner_sign_up.config(text="Enter your name")
            error = True
        elif len(username_val) < 3 or len(username_val) > 10:
            alert_banner_sign_up.config(text="Usernames must be 3 - 10 characters")
            error = True
        elif check_if_user_exist(username_val):
            alert_banner_sign_up.config(text="ERROR: Username already exists")
            error = True
        elif len(password_val) < 5:
            alert_banner_sign_up.config(text="Password must be 6 characters long")
            error = True

        if not error:
            print("******* Sign up *******")
            print("Name entered:", name_val)
            print("Username entered:", username_val)
            print("Password entered:", password_val)
            global cur_user
            cur_user = username_val
            cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (username_val, name_val, password_val, level_val))
            connection.commit()
            sign_up_successful()

    # Build the sign-up window UI
    header_sign_up = Label(signup_window, text="Sign up", bg="green", fg="white", width=300, font="bold")
    header_sign_up.pack()

    alert_banner_sign_up = Label(signup_window, text="", bg="white", fg="red", width=300, font="bold")
    alert_banner_sign_up.pack()

    nameLabel_sign_up = Label(signup_window, text="Name *", bg="white", fg="green")
    nameLabel_sign_up.place(x=20, y=40)
    name_var = StringVar()
    nameEntry_sign_up = Entry(signup_window, textvariable=name_var, bg="white", fg="green", insertbackground="green")
    nameEntry_sign_up.place(x=100, y=42)

    usernameLabel_sign_up = Label(signup_window, text="Username *", bg="white", fg="green")
    usernameLabel_sign_up.place(x=20, y=80)
    username_var = StringVar()
    usernameEntry_sign_up = Entry(signup_window, textvariable=username_var, bg="white", fg="green", insertbackground="green")
    usernameEntry_sign_up.place(x=100, y=82)

    passwordLabel_sign_up = Label(signup_window, text="Password *", bg="white", fg="green")
    passwordLabel_sign_up.place(x=20, y=120)
    password_var = StringVar()
    passwordEntry_sign_up = Entry(signup_window, textvariable=password_var, show='•', bg="white", fg="green", insertbackground="green")
    passwordEntry_sign_up.place(x=100, y=122)

    signUpButton_sign_up = Button(signup_window, text="Sign up", width=8, height=1, bg="white", fg="green",
                                  command=user_credential_sign_up)
    signUpButton_sign_up.place(x=105, y=170)

    loginButton_sign_up = Button(signup_window, text="Cancel", width=5, height=1, bg="white", fg="green", command=go_back_to_login)
    loginButton_sign_up.place(x=210, y=170)

def getuser():
    return cur_user

if __name__ == "__main__":
    main_login_page()
