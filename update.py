import psycopg2 
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import io

# Function to select an image from the file system
def select_image():
    global image_data
    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.jpg;*.png")]
    )
    
    if image_path:
        # Read the selected image in binary mode
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Display the selected image in the interface
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((150, 150))  # Adjust image size
        img_tk = ImageTk.PhotoImage(image)
        image_label.config(image=img_tk)
        image_label.image = img_tk

# Function to load game data into input fields
def load_data():
    game_id = entry_id.get()

    if not game_id:
        messagebox.showerror("Error", "You must enter the game ID to update.")
        return

    try:
        # Connect to the database
        conn = psycopg2.connect("dbname=test1 user=postgres password=1977 host=localhost")
        cur = conn.cursor()

        # Query the game by ID
        cur.execute("SELECT name, description, console, release_year, number_of_players, image FROM games WHERE code = %s;", (game_id,))
        game = cur.fetchone()

        if game:
            # Populate the fields with the game data
            entry_name.delete(0, tk.END)
            entry_name.insert(0, game[0])
            entry_description.delete(0, tk.END)
            entry_description.insert(0, game[1])
            entry_console.delete(0, tk.END)
            entry_console.insert(0, game[2])
            entry_release_year.delete(0, tk.END)
            entry_release_year.insert(0, game[3])
            entry_num_players.delete(0, tk.END)
            entry_num_players.insert(0, game[4])

            # Display the current image
            if game[5]:
                global image_data
                image_data = game[5]
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((150, 150))
                img_tk = ImageTk.PhotoImage(image)
                image_label.config(image=img_tk)
                image_label.image = img_tk
        else:
            messagebox.showinfo("Info", "No game found with the provided ID.")
        
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the data: {e}")

# Function to update game data
def update_data():
    game_id = entry_id.get()
    name = entry_name.get()
    description = entry_description.get()
    console = entry_console.get()
    release_year = entry_release_year.get()
    num_players = entry_num_players.get()

    if not (game_id and name and description and console and release_year and num_players):
        messagebox.showerror("Error", "All fields must be completed.")
        return

    try:
        # Connect to the database
        conn = psycopg2.connect("dbname=test1 user=postgres password=123456 host=localhost")
        cur = conn.cursor()

        # Update the game data
        cur.execute("""
            UPDATE games
            SET name = %s, description = %s, console = %s, release_year = %s, number_of_players = %s, image = %s
            WHERE code = %s;
        """, (name, description, console, release_year, num_players, image_data, game_id))

        conn.commit()

        messagebox.showinfo("Success", "The game has been updated successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating the data: {e}")

# Main window configuration
root = tk.Tk()
root.title("Update Game Data")
root.geometry("500x600")

# Variables
image_data = None

# Labels and input fields
tk.Label(root, text="Game ID:").pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

tk.Button(root, text="Load Data", command=load_data).pack(pady=5)

tk.Label(root, text="Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

tk.Label(root, text="Description:").pack(pady=5)
entry_description = tk.Entry(root)
entry_description.pack(pady=5)

tk.Label(root, text="Console:").pack(pady=5)
entry_console = tk.Entry(root)
entry_console.pack(pady=5)

tk.Label(root, text="Release Year:").pack(pady=5)
entry_release_year = tk.Entry(root)
entry_release_year.pack(pady=5)

tk.Label(root, text="Number of Players:").pack(pady=5)
entry_num_players = tk.Entry(root)
entry_num_players.pack(pady=5)

# Display current or selected image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Button to select a new image
tk.Button(root, text="Select Image", command=select_image).pack(pady=10)

# Button to update data
tk.Button(root, text="Update", command=update_data).pack(pady=20)

# Start the interface
root.mainloop()
