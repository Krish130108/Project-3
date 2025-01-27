import sqlite3

connection = sqlite3.connect("Database.db")

cursor = connection.cursor()
def game(username):
    print("game is now running...")
    cursor.execute(f"SELECT * FROM Users WHERE username == '{username}'")
    details = cursor.fetchall()
    details = details[0]

    username = details[0]
    name = details[1]
    level = details[3]

    #  username name and level are variables above
        





    # SHREY ADD YOU CODE ********* HERE *********
    # IN THE FUNCTION