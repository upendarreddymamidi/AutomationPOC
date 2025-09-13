import shutil
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def convert_to_zip(user_id):
    destination_folder = os.getenv("SCREENSHOT_ZIP_FOLDER")

    if not destination_folder:
        print("Error: screenshot_zip_folder is not set in the .env file.")
        return

    user_folder = f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}"

    zip_file_path = os.path.join(destination_folder, f"{user_id}.zip")
    shutil.make_archive(zip_file_path.replace(".zip", ""), "zip", user_folder)

    print(f"Created zip file: {zip_file_path}")


def make_sreenshot_folders(user_id):
    screenshot_folder = os.getenv("SCREENSHOT_FOLDER")
    user_folder = f"{screenshot_folder}/{user_id}"
    success_folder = os.path.join(user_folder, "success")
    error_folder = os.path.join(user_folder, "error")

    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)

    os.makedirs(success_folder)
    os.makedirs(error_folder)
