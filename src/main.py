import sys
import os

if getattr(sys, 'frozen', False):
    # PyInstaller temp folder
    base_path = sys._MEIPASS

    # Point Tkinter to the extracted Tcl/Tk folders
    os.environ['TCL_LIBRARY'] = os.path.join(base_path, '_tcl_data', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(base_path, '_tk_data', 'tk8.6')

from src.gui import create_main_window


def main():
    app = create_main_window()
    app.mainloop()


if __name__ == "__main__":
    main()
