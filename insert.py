import psycopg2 
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to insert data into the database
def insert_game():
    name = entry_name.get()
    description = entry_description.get()
    console = entry_console.get()
    release_year = entry_release_year.get()
    number_of_players = entry_players.get()
    
    if not name or not description or not console or not release_year or not number_of_players or not image_path:
        messagebox.showerror("Error", "Please fill in all fields and select an image.")
        return

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        conn = psycopg2.connect("dbname=test1 user=postgres password=1977 host=localhost")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO games (Name, Description, Console, Release_Year, Number_of_Players, Image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, description, console, release_year, number_of_players, image_data))

        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Success", "Game inserted successfully.")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while inserting the game: {e}")

# Function to select the image
def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("JPG Image", "*.jpg"), ("PNG Image", "*.png")])
    if image_path:
        image = Image.open(image_path)
        image.thumbnail((150, 150))
        img = ImageTk.PhotoImage(image)
        label_image.config(image=img)
        label_image.image = img

# Function to clear text fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_console.delete(0, tk.END)
    entry_release_year.delete(0, tk.END)
    entry_players.delete(0, tk.END)
    label_image.config(image='')

# Create the main window
root = tk.Tk()
root.title("Insert Game")

# Variables to store the image path
image_path = None

# Create labels and entry fields
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

label_description = tk.Label(root, text="Description:")
label_description.grid(row=1, column=0)
entry_description = tk.Entry(root)
entry_description.grid(row=1, column=1)

label_console = tk.Label(root, text="Console:")
label_console.grid(row=2, column=0)
entry_console = tk.Entry(root)
entry_console.grid(row=2, column=1)

label_release_year = tk.Label(root, text="Release Year:")
label_release_year.grid(row=3, column=0)
entry_release_year = tk.Entry(root)
entry_release_year.grid(row=3, column=1)

label_players = tk.Label(root, text="Number of Players:")
label_players.grid(row=4, column=0)
entry_players = tk.Entry(root)
entry_players.grid(row=4, column=1)

# Button to select an image
btn_select_image = tk.Button(root, text="Select Image", command=select_image)
btn_select_image.grid(row=5, column=0, columnspan=2)

# Label to display the selected image
label_image = tk.Label(root)
label_image.grid(row=6, column=0, columnspan=2)

# Button to insert the game into the database
btn_insert = tk.Button(root, text="Insert Game", command=insert_game)
btn_insert.grid(row=7, column=0, columnspan=2)

# Start the application
root.mainloop()
