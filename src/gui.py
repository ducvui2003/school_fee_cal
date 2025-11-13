import os
import tkinter as tk
from tkinter import filedialog, messagebox
from src.const import (
    APP_NAME,
    APP_SIZE,
    TEMPLATE_FILE,
    SETTINGS_FOLDER,
    DOWNLOAD_FOLDER,
)
from src.core import generate_bills_from_html, merge_pdfs_in_folder
from src.settings import app_settings
from src.utils import get_cur_datetime
from src.text import (
    SELECT_FILE_PLACEHOLDER,
    EMPTY_FILE_NAME,
    CHOOSE_FILE,
    CREATE_PDF,
    CREATE_SUCCESS,
    PDF_OUTPUT_MSG,
)

selected_excel_file = None


def generate_bills_click(output_folder):
    excel_path = selected_excel_file
    if not os.path.exists(excel_path):
        messagebox.showerror("Error", f"Excel file not found:\n{excel_path}")
        return

    try:
        unique_name = get_cur_datetime()
        folder_dump_path = os.path.join(app_settings.get("history"), unique_name)
        file_pdf_merge_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_name}.pdf")
        generate_bills_from_html(
            excel_path=excel_path, template_path=TEMPLATE_FILE, output_folder=folder_dump_path
        )

        merge_pdfs_in_folder(folder_path=folder_dump_path, output_path=file_pdf_merge_path)

        messagebox.showinfo(CREATE_SUCCESS, PDF_OUTPUT_MSG.format(output_folder))

        os.startfile(output_folder)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDFs:\n{e}")


# Create menu
def create_menu(root):
    # -----------------------------
    # Menu bar
    # -----------------------------
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Settings menu
    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=settings_menu)

    def open_settings():
        """Open settings dialog to select output folder."""
        new_folder = filedialog.askdirectory(
            title="Select default output folder", initialdir=SETTINGS_FOLDER
        )
        if new_folder:
            app_settings.set('output_folder')
            messagebox.showinfo("Settings Saved", f"New output folder:\n{new_folder}")

    settings_menu.add_command(label="Set Output Folder", command=open_settings)


def choose_file(label):
    """Open file dialog to choose Excel file and update label"""
    global selected_excel_file
    file_path = filedialog.askopenfilename(
        title=SELECT_FILE_PLACEHOLDER, filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    print(file_path)
    if file_path:
        selected_excel_file = file_path

        label.config(text=os.path.basename(file_path))


def create_main_window():
    # Create main window
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry(APP_SIZE)
    create_menu(root)

    # Label to show selected file
    file_label = tk.Label(root, text=EMPTY_FILE_NAME)
    file_label.pack(pady=10)

    # Button to choose Excel file
    btn_choose = tk.Button(root, text=CHOOSE_FILE, command=lambda: choose_file(file_label))
    btn_choose.pack(pady=10)

    output_folder = DOWNLOAD_FOLDER
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    btn_generate = tk.Button(
        root,
        text=CREATE_PDF,
        command=lambda: generate_bills_click(output_folder),
        height=2,
        width=25,
    )
    btn_generate.pack(pady=50)

    return root
