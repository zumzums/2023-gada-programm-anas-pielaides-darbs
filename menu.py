import tkinter as tk
import os
import sqlite3

#globalais prieks speletaja
current_player = None

def register():
    global current_player
    
    username = username_entry.get()
    password = password_entry.get()
    
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    
    #uztaisa tabulu, ja tada nav
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # parbauda vai speletajs jau eksiste
    query = "SELECT * FROM users WHERE username = ?"
    values = (username,)
    cursor.execute(query, values)
    user = cursor.fetchone()
    if user:
        print("User already exists")
        return
    current_player = username
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    values = (username, password)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    #palaiz spēles kodu
    os.system('python main.py')

root = tk.Tk()
root.title("Game Menu")
root.geometry("300x200")

username_label = tk.Label(root, text="Username")
username_label.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password")
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

root.mainloop()
