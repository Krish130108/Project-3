import sqlite3
from tkinter import *
from functools import partial
from Levels import *


connection = sqlite3.connect("Database.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Users (username TEXT PRIMARY KEY, name TEXT, password TEXT, level INT)")


root = Tk()
root.geometry('300x400')
  
root.configure(background="white")


def main_login_page():
    def user_credential_Login(username, password):
        username = username.get()
        password = password.get()

        if len(username) and len(password) > 0:

            user_exist = check_if_user_exist(username)
            if user_exist == True:
                
                cursor.execute(f"SELECT password FROM Users WHERE username == '{username}'")
                user_password = cursor.fetchall()

                if password == str(user_password)[3:-4]:
                    alert_banner_Login.config(text="")
                    
                    print("******* Login *******")
                    print("Username entered :", username)
                    print("Password entered :", password)
                    root.destroy()
                    level_page(username)
                    
                else:
                    alert_banner_Login.config(text="Wrong username or password")                    
            else:
                alert_banner_Login.config(text="Wrong username or password")
        else:
            alert_banner_Login.config(text="Fill in the required fields!")
        

    def check_if_user_exist(username):
            cursor.execute(f"SELECT * FROM Users WHERE username == '{username}'")
            found = cursor.fetchall()
            if len(found) == 1:                  
                return True
            else:
                return False


    def sign_up_page():
        header_Login.destroy()
        alert_banner_Login.destroy()
        usernameLabel_Login.destroy()
        usernameEntry_Login.destroy()
        passwordLabel_Login.destroy()
        passwordEntry_Login.destroy()
        loginButton_Login.destroy()
        signUpButton_Login.destroy()
        

        def go_to_main_login_page():
            header_sign_up.destroy()
            alert_banner_sign_up.destroy()
            nameLabel_sign_up.destroy()
            nameEntry_sign_up.destroy()
            usernameLabel_sign_up.destroy()
            usernameEntry_sign_up.destroy()
            passwordLabel_sign_up.destroy()
            passwordEntry_sign_up.destroy()
            loginButton_sign_up.destroy()
            signUpButton_sign_up.destroy()
            main_login_page()
        
        
        def sign_up_successful():
            alert_banner_sign_up.destroy()
            nameLabel_sign_up.destroy()
            nameEntry_sign_up.destroy()
            usernameLabel_sign_up.destroy()
            usernameEntry_sign_up.destroy()
            passwordLabel_sign_up.destroy()
            passwordEntry_sign_up.destroy()
            loginButton_sign_up.destroy()
            signUpButton_sign_up.destroy()

            def go_to_main_login_page_after_confrimation():
                header_sign_up.destroy()
                lable_sign_up_successful.destroy()
                confirm_button_sign_up.destroy()
                main_login_page()

            header_sign_up.config(text='Sign up successful')
            lable_sign_up_successful = Label(root, text=f'You have successfully signed up\n\nYou can now sign in with your new account.', bg="white", fg="green")
            
            lable_sign_up_successful.pack()

            confirm_button_sign_up = Button(root, text="Back to Login", width=8, height=1, bg="white", fg='green', padx=0, pady=0, command=go_to_main_login_page_after_confrimation)
            confirm_button_sign_up.pack()

            
        def user_credential_sign_up(name, username, password):
            name = name.get()
            username = username.get()
            password = password.get()
            level = 1

            error = False
            
            if len(name) <= 2:
                alert_banner_sign_up.config(text="Enter your name")
                error = True
            elif len(username) < 3 or len(username) > 10:
                alert_banner_sign_up.config(text='Usernames must be 3 - 10 characters ')
                error = True
            elif check_if_user_exist(username) == True:
                alert_banner_sign_up.config(text="ERROR: Username already exist")
                error = True
            elif len(password) < 5:
                alert_banner_sign_up.config(text="Password must be 6 character long")
                error = True

            if error != True:
                print("******* Sign up *******")
                print("name entered :", name)
                print("username entered :", username)
                print("password entered :", password)

                cursor.execute(f"INSERT INTO Users VALUES ('{username}' , '{name}' , '{password}', '{level}' )")
                connection.commit()
                sign_up_successful()
            

        root.title("Cannon Game - Sign up")  

        header_sign_up = Label(root, text="Sign up", bg="green", fg='white',  width=300, font='bold')
        header_sign_up.pack()

        alert_banner_sign_up = Label(root, text="", bg="white", fg='red',  width=300, font='bold')
        alert_banner_sign_up.pack()

        nameLabel_sign_up = Label(root, text="Name *", bg="white", fg='green')
        nameLabel_sign_up.place(x=20,y=40)
        name = StringVar()
        nameEntry_sign_up = Entry(root, textvariable=name, bg="white", fg='green', insertbackground="green")
        nameEntry_sign_up.place(x=100,y=42) 

        usernameLabel_sign_up = Label(root, text="Username *", bg="white", fg='green')
        usernameLabel_sign_up.place(x=20,y=80)
        username = StringVar()
        usernameEntry_sign_up = Entry(root, textvariable=username, bg="white", fg='green', insertbackground="green")
        usernameEntry_sign_up.place(x=100,y=82) 

        passwordLabel_sign_up = Label(root,text="Password *", bg="white", fg='green')
        passwordLabel_sign_up.place(x=20,y=120) 
        password = StringVar()
        passwordEntry_sign_up = Entry(root, textvariable=password, show='•', bg="white", fg='green', insertbackground="green")
        passwordEntry_sign_up.place(x=100,y=122)

        user_credential_sign_up = partial(user_credential_sign_up, name, username, password)

        signUpButton_sign_up = Button(root, text="Sign up", width=8, height=1, bg="white", fg='green', padx=0, pady=0, command=user_credential_sign_up)
        signUpButton_sign_up.place(x=105,y=170)

        loginButton_sign_up = Button(root, text="Login", width=5, height=1, bg="white", fg='green', padx=0, pady=0, command=go_to_main_login_page)
        loginButton_sign_up.place(x=210,y=170)

    root.title("Cannon Game - Login")  

    header_Login = Label(root, text="Login", bg="green", fg='white',  width=300, font='bold')
    header_Login.pack()

    alert_banner_Login = Label(root, text="", bg="white", fg='red',  width=300, font='bold')
    alert_banner_Login.pack()

    usernameLabel_Login = Label(root, text="Username *", bg="white", fg='green')
    usernameLabel_Login.place(x=20,y=40)
    username = StringVar()
    usernameEntry_Login = Entry(root, textvariable=username, bg="white", fg='green', insertbackground="green")
    usernameEntry_Login.place(x=100,y=42) 
    #password label and password entry box

    passwordLabel_Login = Label(root,text="Password *", bg="white", fg='green')
    passwordLabel_Login.place(x=20,y=80)  
    password = StringVar()
    passwordEntry_Login = Entry(root, textvariable=password, show='*', bg="white", fg='green', insertbackground="green")
    passwordEntry_Login.place(x=100,y=82)  

    user_credential_Login = partial(user_credential_Login, username, password)

    #login button

    loginButton_Login = Button(root, text="Login", width=8, height=1, command=user_credential_Login, bg="white", fg='green')
    loginButton_Login.place(x=100,y=130)  

    signUpButton_Login = Button(root, text="Sign up", width=5, height=1, command=sign_up_page, bg="white", fg='green')
    signUpButton_Login.place(x=210,y=130)

    root.mainloop()

main_login_page()