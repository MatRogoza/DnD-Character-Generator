import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from create_menu import create_menu
import os
from Class_Features import populate_database


def initialize_database():
    db_path = 'dnd_character_info.db'
    
    # Check if the database exists or is empty
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        print("Database is empty. Populating...")
        populate_database()  # Call the function to populate the database
    else:
        print("Database is already populated.")

# Call this function before launching the main program
initialize_database()

# Your existing login menu logic here...

#Connect to the Sqlite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

#Create a table for storing user accounts
c.execute('''
 CREATE TABLE IF NOT EXISTS users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     username TEXT NOT NULL UNIQUE,
     password TEXT NOT NULL
 )
 ''')
conn.commit()

#Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = entry_username.get()
    password = entry_password.get()

    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()

    if result and result[0] == hash_password(password):
        messagebox.showinfo('Login Successful', f"Welcome {username}!")
        login_window.withdraw() #Hide the login window
        main_menu() #Call the main menu function
    else:
        messagebox.showerror('Login Failed', 'Invalid username or password.')

#Function to handle account creation
def create_account():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, hash_password(password)))
            conn.commit()
            messagebox.showinfo('Account Created', f'Account for {username} has been created.')
        except sqlite3.IntegrityError:
            messagebox.showerror('Error', 'Username already exists. Please choose a different one.')
    else:
        messagebox.showerror('Error', "Please enter a username and password.")  


#Main Menu Function
def main_menu():
    main_window = tk.Toplevel() #Create a new window
    main_window.title("Mat's D&D Character Sheet")
    main_window.geometry('500x500')

    def create_character():
        messagebox.showinfo('Character Creator', "Forward to Character Creator!")
        main_window.withdraw() #Hide the main window
        create_menu()

    def view_character():
        messagebox.showinfo('Characters', 'Forward to existing Characters!')

    def edit_character():
        messagebox.showinfo('Character Editor', 'Forward to Character Editor!')

    def on_closing():
        if messagebox.askyesno('Quit?', 'Do you really want to log out?'):
            main_window.destroy()
            login_window.deiconify() #brings back the login menu

    #Widgets of Main Menu
    button_create = tk.Button(main_window, text="Create a Character", command=create_character)
    button_view = tk.Button(main_window, text="View your Characters", command=view_character)
    button_edit = tk.Button(main_window, text='Edit your Characters', command=edit_character)
    button_logout = tk.Button(main_window, text='Logout', command=on_closing)

    button_create.pack(padx=5, pady=5)
    button_view.pack(padx=5, pady=5)
    button_edit.pack(padx=5, pady=5)
    button_logout.pack(padx=5, pady=5)
    
    center_window(main_window, 500, 500)
    


def center_window(window, width, height): #function to center window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry(f'{width}x{height}+{x}+{y}')

def close_login_window():
    conn.close()
    login_window.destroy()


#Create the login window      
login_window = tk.Tk()
login_window.title('Login')
login_window.geometry('300x200')

label_username = tk.Label(login_window, text="Username:")
label_password = tk.Label(login_window, text="Password:")

entry_username = tk.Entry(login_window)
entry_password = tk.Entry(login_window, show="*")

button_login = tk.Button(login_window, text="Login", command=login)
button_create_account = tk.Button(login_window, text="Create Account", command=create_account)

label_username.grid(row=0, column=0, padx=10, pady=10)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password.grid(row=1, column=1, padx=10, pady=10)

button_login.grid(row=2, column=0, padx=10, pady=10)
button_create_account.grid(row=2, column=1, padx=10, pady=10)

center_window(login_window, 300, 200)
login_window.protocol("WM_DELETE_WINDOW", close_login_window)
login_window.mainloop()


