import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))  # folder where the current script lives
TEMPLATE_FILE = os.path.join(os.getcwd(), "templates", "bill_template.docx")
OUTPUT_DIR = os.path.join(os.getcwd(), "templates", "bill_template.docx")
WKHTMLTOPDF_PATH = os.path.join(curr_dir, "..", "libs", "wkhtmltopdf.exe")
ROOT_PATH = os.path.normpath(
    os.path.join(
        curr_dir,
        "..",
    )
)

APP_NAME = 'Tính tiền học Hạnh Phúc (AP)'
APP_SIZE = '600x300'

TEMPLATE_FILE = os.path.join(curr_dir, "..", "templates", "bill_template.html")
FONT_FILE = os.path.join(curr_dir, "..", "fonts", "bill_template.html")

OUTPUT_DIR = os.path.join(curr_dir, "..", "test", "out")
SETTINGS_FOLDER = os.path.join(os.getenv("APPDATA"), "hanh_phuc_school")

os.makedirs(SETTINGS_FOLDER, exist_ok=True)
SETTINGS_FILE = os.path.join(SETTINGS_FOLDER, "settings.json")
HISTORY_FOLDER = os.path.join(SETTINGS_FOLDER, "history")
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# Detect if running as frozen EXE (e.g., PyInstaller build)
IS_FROZEN = getattr(sys, 'frozen', False)

# Environment (dev/prod)
if IS_FROZEN:
    APP_ENV = "prod"
else:
    APP_ENV = os.getenv("APP_ENV", "dev")

# Simple debug flag
DEBUG = APP_ENV == "dev"
