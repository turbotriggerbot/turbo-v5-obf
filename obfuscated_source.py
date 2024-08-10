import os
from pathlib import Path
import importlib
from subprocess import call
import subprocess
import sys
import os



required_packages = [
    'requests',
    "win32api",
    "ctypes"
]




def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages(packages):
    installed = True
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing now...")
            if package == "win32api":
                package = "pywin32"
            install(package)
            installed = False
    return installed

if check_and_install_packages([pkg.split('==')[0] for pkg in required_packages]):
    # All packages are installed, proceed with the script
    print("All required packages are installed!")

    # Example main script code
    import requests
    # Your script logic here
    print("Script is running...")
else:
    # Packages were installed, restart the script
    print("Restarting the script to apply changes...")
    os.execv(sys.executable, ['python'] + sys.argv)


try:
    os.system('cls')
    import requests
    import ctypes
    import win32com.client
    print('''
    -----------------------------------------------------------------------------------------
     HOW TO RUN THE SCRIPT
     1. wait for the script to open the folder with the script ("turbo" in the desktop)
     2. right click run_this_as_admin file
     3. choose "run as administrator"
    -----------------------------------------------------------------------------------------
          
    ''')
    # Step 1: Get the desktop path and add the 'turbo' folder to it
    def get_desktop():
        CSIDL_DESKTOP = 0x0000  # Desktop
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value

        buf = ctypes.create_unicode_buffer(260)  # MAX_PATH is usually 260 characters
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)

        return Path(buf.value)

    desktop_path = get_desktop()
    turbo_folder_path = desktop_path / "turbo"

    # Step 2: Create the 'turbo' folder if it doesn't already exist
    if not turbo_folder_path.exists():
        turbo_folder_path.mkdir()
        print(f"Folder created: {turbo_folder_path}")
    else:
        print(f"Folder already exists: {turbo_folder_path}")

    # Step 3: Fetch the Python script from the URL and save it
    url = "https://raw.githubusercontent.com/turbotriggerbot/turbo-v5-obf/main/obfuscated_source_customer.py"
    python_script_path = turbo_folder_path / "turbo_script.py"

    response = requests.get(url)
    if response.status_code == 200:
        with python_script_path.open("w") as file:
            file.write(response.text)
        print(f"Python script downloaded and saved to: {python_script_path}")
    else:
        print(f"Failed to download Python script. Status code: {response.status_code}")
        exit()

    # Step 4: Create the batch file
    bat_file_path = turbo_folder_path / "run_this_as_admin.bat"

    with bat_file_path.open("w") as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'cd /d "{turbo_folder_path}"\n')
        bat_file.write(f'python "{python_script_path.name}"\n')
        bat_file.write(f'pause\n')  # Optional: keep the console window open after the script runs

    print(f"Batch file created: {bat_file_path}")
    import subprocess
    subprocess.run(['explorer', str(turbo_folder_path)])
    import time
    time.sleep(100)
except Exception as e:
    print(f"An error occurred: {e}")
    time.sleep(10000)