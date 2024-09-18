import psycopg2
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import io

# Global variables to handle record index
results = []
current_index = 0

# Function to display the data of a specific game based on the index
def show_data(index):
    if results and 0 <= index < len(results):
        row = results[index]
        
        code.set(f"Code: {row[0]}")
        name.set(f"Name: {row[1]}")
        description.set(f"Description: {row[2]}")
        console.set(f"Console: {row[3]}")
        release_year.set(f"Release Year: {row[4]}")
        num_players.set(f"Number of Players: {row[5]}")

        # If there is an image, show it
        if row[6] is not None:
            image_data = row[6]
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((250, 250))  # Adjust image size
            img_tk = ImageTk.PhotoImage(image)
            image_label.config(image=img_tk)
            image_label.image = img_tk
    else:
        clear_fields()

# Function to load all data
def show_all():
    global results, current_index
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect("dbname=test1 user=postgres password=1977 host=localhost")
        cur = conn.cursor()

        # Query all data from the games table
        cur.execute("SELECT code, name, description, console, release_year, number_of_players, image FROM games;")
        results = cur.fetchall()

        if results:
            current_index = 0  # Reset the index
            show_data(current_index)  # Show the first record
        else:
            messagebox.showinfo("Information", "No data found in the database.")
        
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while querying the data: {e}")

# Function to move to the next record
def next_record():
    global current_index
    if current_index < len(results) - 1:
        current_index += 1
        show_data(current_index)
    else:
        messagebox.showinfo("Information", "No more records.")

# Function to move to the previous record
def previous_record():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_data(current_index)
    else:
        messagebox.showinfo("Information", "This is the first record.")

# Function to clear the fields in the interface
def clear_fields():
    code.set("Code: ")
    name.set("Name: ")
    description.set("Description: ")
    console.set("Console: ")
    release_year.set("Release Year: ")
    num_players.set("Number of Players: ")
    image_label.config(image='')

# Main window configuration
root = tk.Tk()
root.title("Game Data")
root.geometry("400x600")

# Variables to display the data
code = tk.StringVar()
name = tk.StringVar()
description = tk.StringVar()
console = tk.StringVar()
release_year = tk.StringVar()
num_players = tk.StringVar()

# Labels to display the data
tk.Label(root, textvariable=code).pack(pady=5)
tk.Label(root, textvariable=name).pack(pady=5)
tk.Label(root, textvariable=description).pack(pady=5)
tk.Label(root, textvariable=console).pack(pady=5)
tk.Label(root, textvariable=release_year).pack(pady=5)
tk.Label(root, textvariable=num_players).pack(pady=5)

# Label to display the image
image_label = Label(root)
image_label.pack(pady=10)

# Button to load all data
tk.Button(root, text="Show All", command=show_all).pack(pady=20)

# Navigation buttons
tk.Button(root, text="Previous", command=previous_record).pack(side=tk.LEFT, padx=20)
tk.Button(root, text="Next", command=next_record).pack(side=tk.RIGHT, padx=20)

# Start the interface
root.mainloop()
