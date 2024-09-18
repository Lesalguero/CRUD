import psycopg2
import tkinter as tk
from tkinter import messagebox

# Function to delete the game from the database
def delete_game():
    game_id = entry_id.get()

    if not game_id:
        messagebox.showerror("Error", "You must enter the ID of the game to delete.")
        return

    # Confirmation before deleting
    response = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the game with ID {game_id}?")
    
    if response:
        try:
            # Connect to the database
            conn = psycopg2.connect("dbname=test1 user=postgres password=1977 host=localhost")
            cur = conn.cursor()

            # Delete the game by ID
            cur.execute("DELETE FROM games WHERE Code = %s;", (game_id,))
            conn.commit()

            # Verify if a record was deleted
            if cur.rowcount > 0:
                messagebox.showinfo("Success", f"The game with ID {game_id} has been deleted.")
            else:
                messagebox.showinfo("Information", f"No game found with ID {game_id}.")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the game: {e}")

# Main window setup
root = tk.Tk()
root.title("Delete Game")
root.geometry("400x200")

# Label and entry field for the game ID
tk.Label(root, text="Enter the Game ID to delete:").pack(pady=10)
entry_id = tk.Entry(root)
entry_id.pack(pady=10)

# Button to delete the game
tk.Button(root, text="Delete Game", command=delete_game, bg="red", fg="white").pack(pady=20)

# Start the interface
root.mainloop()
