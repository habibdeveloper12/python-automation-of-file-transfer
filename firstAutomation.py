import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the Downloads folder path
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# Define file categories with extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".pptx", ".txt", ".csv"],
    "Executables": [".exe", ".msi"],
    "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Others": []
}

# Function to determine destination folder
def get_destination(file_name):
    file_ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in CATEGORIES.items():
        if file_ext in extensions:
            return os.path.join(DOWNLOADS_FOLDER, category)
    return os.path.join(DOWNLOADS_FOLDER, "Others")

# Function to avoid overwriting files
def get_unique_filename(destination_folder, file_name):
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    new_file_path = os.path.join(destination_folder, new_file_name)

    while os.path.exists(new_file_path):  # If file already exists, rename it
        new_file_name = f"{base_name} ({counter}){extension}"
        new_file_path = os.path.join(destination_folder, new_file_name)
        counter += 1

    return new_file_path

# Function to move files safely
def move_file(file_path):
    if not os.path.isfile(file_path):
        return
    
    file_name = os.path.basename(file_path)
    dest_folder = get_destination(file_name)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create the folder if it doesn't exist

    # Get a unique file name to prevent overwriting
    new_path = get_unique_filename(dest_folder, file_name)

    # Move the file
    shutil.move(file_path, new_path)
    print(f"Moved: {file_name} → {new_path}")

# Watchdog event handler
class DownloadsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        time.sleep(1)  # Small delay to prevent issues
        move_file(event.src_path)

# Function to start monitoring
def monitor_downloads():
    event_handler = DownloadsHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()
    print(f"🚀 Monitoring {DOWNLOADS_FOLDER}...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run script
if __name__ == "__main__":
    monitor_downloads()
