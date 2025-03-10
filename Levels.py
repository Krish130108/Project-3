import customtkinter as ctk
from PIL import Image
import sqlite3
import os 

connection = sqlite3.connect("Database.db")

cursor = connection.cursor()

def level_page(username):
    print("game is now running...")
    print(username)
    cursor.execute(f"SELECT * FROM Users WHERE username == '{username}'")
    details = cursor.fetchall()
    details = details[0]

    username = details[0]
    user_level = details[3]


    def lvl_checker(level, user_level):
      
      if user_level >= level :
          print('level:', level)
          main.destroy()
          os.system("python main.py")        

      else:
          error_label = ctk.CTkLabel(main,text = "USER DOES NOT MEET LEVEL REQUIRED",text_color= "#e32619",fg_color="#ADD8E6")
          error_label.place(relx = 0.42,rely = 0.9)
          error_label.after(4000, lambda: error_label.destroy())
          # .destroy() is the function destroys the label and 4000 is the milliseconds the label is displayed
          

    def initialize_main_window():
        main = ctk.CTk()
        main.title("Cannon game - Levels")

        # Calculate window size based on screen
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        main.geometry(f"{window_width}x{window_height}")
        

        # Set appearance and theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        return main

    def clear_window(window):
        for widget in window.winfo_children():
            widget.destroy()

    def main_screen(main):
        clear_window(main)
        
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        #lvl = ctk.StringVar(value = "1")
        

        lvl_background = ctk.CTkImage(light_image = Image.open('assets/sky.png'),dark_image = Image.open('assets/sky.png'),size = (window_width*2,window_height*2))
        lvl_label = ctk.CTkLabel(main,text = "",image = lvl_background)
        lvl_label.place(relx= 0,rely = 0)

        title = ctk.CTkImage(light_image= Image.open('assets/Canon_title.png'),dark_image = Image.open('assets/Canon_title.png'),size = (window_width*0.3,window_height*0.4) )
        title_label = ctk.CTkLabel(main,image = title)
        title_label.place(relx = 0.42, rely = 0.10)

    
        button_lvl_1 = ctk.CTkButton(main, text="LEVEL 1", font=("Arial", 16), fg_color = "#ADD8E6",hover_color = "#43e8d8",command = lambda:lvl_checker(1,user_level))
        button_lvl_1.place(relx=0.5, rely=0.4, anchor="center")

        button_lvl_2 = ctk.CTkButton(main, text="LEVEL 2", font=("Arial", 16), fg_color = "#ADD8E6",hover_color = "#43e8d8",command = lambda:lvl_checker(2,user_level) )
        button_lvl_2.place(relx=0.5, rely=0.5, anchor="center")

        button_lvl_3 = ctk.CTkButton(main, text="LEVEL 3", font=("Arial", 16), fg_color = "#ADD8E6",hover_color = "#43e8d8",command = lambda:lvl_checker(3,user_level))
        button_lvl_3.place(relx=0.5, rely=0.6, anchor="center")

        button_lvl_4 =ctk.CTkButton(main, text="LEVEL 4", font=("Arial", 16), fg_color = "#ADD8E6",hover_color = "#43e8d8",command = lambda:lvl_checker(4,user_level) )
        button_lvl_4.place(relx=0.5, rely=0.7, anchor="center")
        
        #, variable = lvl
        #,value = "1"  

    
    main = initialize_main_window()
    main_screen(main)
    main.mainloop()

