import os
import shutil
from datetime import datetime
from plyer import notification

# --- CONFIGURATION ---
# Use the 'r' before the quotes for Windows paths!
SOURCE_DIR = r'C:\Users\Nia\OneDrive\Desktop\Messy_Photos'
DEST_DIR = r'C:\Users\Nia\OneDrive\Desktop\Organized_Photos'

def run_organizer():
    # print("DEBUG: Function started...")
    print(f"🚀 Starting Chronos Organizer...")
    print(f"📂 Scanning: {SOURCE_DIR}")

    # Create destination if it doesn't exist
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"📁 Created main destination folder: {DEST_DIR}")

    moved_count = 0

    # Loop through the files
    for filename in os.listdir(SOURCE_DIR):
        # Filter for images
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(SOURCE_DIR, filename)

            # Get the date the file was last changed
            timestamp = os.path.getmtime(file_path)
            date_obj = datetime.fromtimestamp(timestamp)

            # Create a folder name like "2024-October"
            folder_name = date_obj.strftime('%Y-%B')
            target_folder = os.path.join(DEST_DIR, folder_name)

            # Create the subfolder if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # --- SAFETY CHECK ---
            # Define exactly where the file is going
            final_destination = os.path.join(target_folder, filename)

            # Check if a file with this name already exists there
            if os.path.exists(final_destination):
                print(f"⚠️  SKIP: '{filename}' already exists in {folder_name}. No move performed.")
                continue  # Skip to the next file in the list

            # Move the file if the check passes
            shutil.move(file_path, final_destination)
            print(f"✅ Moved: {filename} -> {folder_name}")
            moved_count += 1

    # Send the Windows notification
    notification.notify(
        title='Chronos Pipeline',
        message=f'Success! {moved_count} files organized.',
        timeout=5
    )
    print(f"\n✨ Task Complete! {moved_count} files moved.")


if __name__ == "__main__":
    run_organizer()