import tkinter as tk
from tkinter import filedialog, messagebox

def create_main_window():
    # Create main window
    root = tk.Tk()
    root.title("File Picker GUI")
    root.geometry("400x200")

    # Label
    label = tk.Label(root, text="Select a file to process")
    label.pack(pady=20)

    # File picker function
    def pick_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                messagebox.showinfo("Success", f"File processed:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process file:\n{e}")

    # Button to pick a file
    btn_pick = tk.Button(root, text="Pick File", command=pick_file)
    btn_pick.pack(pady=10)

    return root