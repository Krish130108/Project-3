import sqlite3

connection = sqlite3.connect("Database.db")

cursor = connection.cursor()

def updateLevel(username, newLevel):
    cursor.execute(f"UPDATE Users SET level = '{newLevel}' WHERE username == '{username}'")
    connection.commit()

