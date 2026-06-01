import os
import sqlite3
import sys
from tkinter import *
from tkinter import messagebox

# Main Login Window
root = Tk()
root.title("Clinic Management Login")
root.geometry("500x400")
root.config(bg="#0B1F3A")

# Title
title = Label(
    root,
    text="COMMUNITY HEALTH SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#0B1F3A",
    fg="white"
)
title.pack(pady=30)

subtitle = Label(
    root,
    text="System Login",
    font=("Arial", 14),
    bg="#0B1F3A",
    fg="lightgray"
)
subtitle.pack(pady=10)

# Variables
username_var = StringVar()
password_var = StringVar()


# Login Function
def login():
    username = username_var.get().strip()
    password = password_var.get().strip()

    # Validation
    if not username or not password:
        messagebox.showerror(
            "Error",
            "Please enter username and password"
        )
        return

    # Database Connection
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # Check User
    cursor.execute('''
    SELECT * FROM users
    WHERE username=? AND password=?
    ''', (username, password))

    user = cursor.fetchone()
    conn.close()

    # If user exists
    if user:
        messagebox.showinfo(
            "Login Success",
            f"Welcome {username}"
        )
        root.destroy()

        # Secure System Execution Pathing
        os.system(f'"{sys.executable}" main.py')
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


# Login Frame
frame = Frame(root, bg="white", padx=30, pady=30)
frame.pack(pady=20)

# Username Layout Elements
Label(
    frame,
    text="Username",
    font=("Arial", 12),
    bg="white"
).grid(row=0, column=0, pady=15, sticky=W)

Entry(
    frame,
    textvariable=username_var,
    width=30,
    font=("Arial", 12)
).grid(row=0, column=1)

# Password Layout Elements
Label(
    frame,
    text="Password",
    font=("Arial", 12),
    bg="white"
).grid(row=1, column=0, pady=15, sticky=W)

Entry(
    frame,
    textvariable=password_var,
    show="*",
    width=30,
    font=("Arial", 12)
).grid(row=1, column=1)

# Interactive Process Trigger Keys Buttons
Button(
    root,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    bg="#1ABC9C",
    fg="white",
    width=20,
    height=2,
    command=login
).pack(pady=20)

Button(
    root,
    text="EXIT",
    font=("Arial", 11, "bold"),
    bg="red",
    fg="white",
    width=15,
    command=root.destroy
).pack()

root.mainloop()