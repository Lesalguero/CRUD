import tkinter as tk
import os

# Functions to open the scripts
def open_update():
    os.system('python update.py')

def open_delete():
    os.system('python delete.py')

def open_insert():
    os.system('python insert.py')

def open_read():
    os.system('python read.py')

# Main window configuration
root = tk.Tk()
root.title("Game Management")
root.geometry("300x300")

# Title label
tk.Label(root, text="Game Management", font=("Helvetica", 16)).pack(pady=20)

# Button to open the update interface
tk.Button(root, text="Update Game", command=open_update, width=20).pack(pady=10)

# Button to open the delete interface
tk.Button(root, text="Delete Game", command=open_delete, width=20).pack(pady=10)

# Button to open the insert interface
tk.Button(root, text="Insert Game", command=open_insert, width=20).pack(pady=10)

# Button to open the read interface
tk.Button(root, text="Read Games", command=open_read, width=20).pack(pady=10)

# Start the interface
root.mainloop()
