import os
import shutil
from datetime import datetime
from plyer import notification

# --- CONFIGURATION ---
# Note: Ensure these folders exist on your Desktop!
SOURCE_DIR = r'C:\Users\Nia\OneDrive\Desktop\Messy_Photos'
DEST_DIR = r'C:\Users\Nia\OneDrive\Desktop\Organized_Photos'


def run_organizer():
    print(f"🚀 Starting Chronos Organizer...")
    print(f"📂 Scanning: {SOURCE_DIR}")

    # 1. PATH VALIDATION
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ ERROR: Source directory {SOURCE_DIR} not found!")
        return

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"📁 Created main destination folder: {DEST_DIR}")

    moved_count = 0

    # 2. FILE PROCESSING LOOP
    for filename in os.listdir(SOURCE_DIR):
        # Ignore hidden system files or folders
        if filename.startswith('.') or not '.' in filename:
            continue

        # Filter for specific image types
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(SOURCE_DIR, filename)

            try:
                # Get the date and format the folder name (e.g., 2024-October)
                timestamp = os.path.getmtime(file_path)
                date_obj = datetime.fromtimestamp(timestamp)
                folder_name = date_obj.strftime('%Y-%B')
                target_folder = os.path.join(DEST_DIR, folder_name)

                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                final_destination = os.path.join(target_folder, filename)

                # 3. COLLISION DETECTION
                if os.path.exists(final_destination):
                    print(f"⚠️  SKIP: '{filename}' already exists in {folder_name}.")
                    continue

                # 4. PERMISSION & MOVE LOGIC
                shutil.move(file_path, final_destination)
                print(f"✅ Moved: {filename} -> {folder_name}")
                moved_count += 1

            except PermissionError:
                print(f"❌ ERROR: {filename} is in use by another program.")
            except Exception as e:
                print(f"❌ UNEXPECTED ERROR with {filename}: {e}")

    # 5. USER FEEDBACK
    notification.notify(
        title='Chronos Pipeline',
        message=f'Success! {moved_count} files organized.',
        timeout=5
    )
    print(f"\n✨ Task Complete! {moved_count} files moved.")


if __name__ == "__main__":
    run_organizer()