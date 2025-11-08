# tasks.py
from invoke import task
import platform
import os

NAME = "HanhPhuc"
ISCC = r'"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"'

P

# Detect the OS
IS_WINDOWS = platform.system() == "Windows"

# Paths depend on OS
PYTHON = "python" if IS_WINDOWS else "python3"
VENV_DIR = ".venv"
VENV_BIN = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin")
VENV_PYTHON = os.path.join(VENV_BIN, "python")
VENV_ACTIVATE = os.path.join(VENV_BIN, "activate")

# 🔧 Paths to your Tcl/Tk installation (adjust as needed)
TCL_PATH = r"C:\Users\ducvu\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
TK_PATH = r"C:\Users\ducvu\AppData\Local\Programs\Python\Python313\tcl\tk8.6"


@task
def env(c):
    """Create virtual environment"""
    print("Creating virtual environment...")
    c.run(f"{PYTHON} -m venv {VENV_DIR}")
    msg = (
        f"Run '{VENV_DIR}\\Scripts\\activate' to activate the venv (Windows)"
        if IS_WINDOWS
        else f"Run 'source {VENV_DIR}/bin/activate' to activate the venv (Linux/macOS)"
    )
    print(msg)


@task
def install(c):
    """Install dependencies from requirements.txt"""
    c.run(f"{VENV_PYTHON} -m pip install -r requirements.txt")


@task
def add(c, name):
    """Add a new package and update requirements.txt"""
    c.run(f"{VENV_PYTHON} -m pip install {name}")
    c.run(f"{VENV_PYTHON} -m pip freeze > requirements.txt")


@task
def remove(c, name):
    """Uninstall a package and update requirements.txt"""
    c.run(f"{VENV_PYTHON} -m pip uninstall -y {name}")
    c.run(f"{VENV_PYTHON} -m pip freeze > requirements.txt")


@task
def freeze(c):
    """Freeze current dependencies to requirements.txt"""
    c.run(f"{VENV_PYTHON} -m pip freeze > requirements.txt")


def _env_with_tk():
    """Return environment dict with Tcl/Tk variables set"""
    env = os.environ.copy()
    env["TCL_LIBRARY"] = TCL_PATH
    env["TK_LIBRARY"] = TK_PATH
    return env


@task
def main(c):
    """Run the main app"""
    print("Running application with Tkinter fix...")
    c.run(f"{VENV_PYTHON} -m src.main", env=_env_with_tk())


@task
def run(c, path):
    """Run the main app"""
    print("Running application with Tkinter fix...")
    c.run(f"{VENV_PYTHON} -m {path}", env=_env_with_tk())


@task
def build(c):
    """Build the app into a standalone EXE"""
    print("🚀 Building executable...")

    cmd = (
        f'python -m PyInstaller '
        '--onedir --windowed '
        f'--name "{NAME}" '
        '--hidden-import=_tkinter '
        '--hidden-import=tkinter '
        '--add-data "C:/Users/ducvu/AppData/Local/Programs/Python/Python313/tcl/tcl8.6;_tcl_data/tcl8.6" '
        '--add-data "C:/Users/ducvu/AppData/Local/Programs/Python/Python313/tcl/tk8.6;_tcl_data/tk8.6" '
        '--add-data "C:/Users/ducvu/AppData/Local/Programs/Python/Python313/DLLs/tcl86t.dll;_tk_data" '
        '--add-data "C:/Users/ducvu/AppData/Local/Programs/Python/Python313/DLLs/tk86t.dll;_tk_data" '
        '--add-data "templates;templates" '
        '--add-data "fonts;fonts" '
        '--add-data "libs;libs" '
        'src/main.py'
    )
    print("Delete old build")
    c.run(f'rmdir /S /Q "./dist"')
    c.run(f'rmdir /S /Q "./build"')
    c.run(cmd, pty=False)
    print("✅ Build complete! Check the /dist folder.")


@task
def installer(c):
    """Build Windows installer with Inno Setup"""
    script = "installer.iss"
    if not os.path.exists(script):
        raise FileNotFoundError("installer.iss not found")
    c.run(f"{ISCC} {script}")
