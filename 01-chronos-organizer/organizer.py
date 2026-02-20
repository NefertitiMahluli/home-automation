import os
import shutil
from datetime import datetime
from plyer import notification

# --- CONFIGURATION ---
# This works for ANY user on ANY Windows computer!
HOME = os.path.expanduser("~")
#if your filepath is linked to OneDrive use this
SOURCE_DIR = os.path.join(HOME, "OneDrive", "Desktop", "Messy_Photos")
DEST_DIR = os.path.join(HOME, "OneDrive", "Desktop", "Organized_Photos")

# *****if not, use this:*****
# SOURCE_DIR = os.path.join(HOME, "Desktop", "Messy_Photos")
# DEST_DIR = os.path.join(HOME, "Desktop", "Organized_Photos")

def run_organizer():
    # 1. Ensure the destination exists
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    # 2. Create a dated CSV filename
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"organization_report_{current_date}.csv"
    report_path = os.path.join(DEST_DIR, filename)

    file_exists = os.path.isfile(report_path)

    # 3. Open the CSV with UTF-8 for emojis
    with open(report_path, "a", encoding="utf-8-sig") as report:
        if not file_exists:
            report.write("Timestamp,Status,File Name,Destination Folder,Details\n")

        print(f"🚀 Starting Chronos Organizer...")
        print(f"📂 Scanning: {SOURCE_DIR}")

        if not os.path.exists(SOURCE_DIR):
            msg = f"{datetime.now()},❌ ERROR,None,None,Source directory not found\n"
            print("❌ ERROR: Source directory not found!")
            report.write(msg)
            return

        moved_count = 0

        # 4. FILE PROCESSING LOOP
        for filename in os.listdir(SOURCE_DIR):
            if filename.startswith('.') or not '.' in filename:
                continue

            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(SOURCE_DIR, filename)

                try:
                    timestamp = os.path.getmtime(file_path)
                    date_obj = datetime.fromtimestamp(timestamp)
                    # Restore the original date format for folders
                    folder_name = date_obj.strftime('%Y-%B')
                    target_folder = os.path.join(DEST_DIR, folder_name)

                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)

                    final_destination = os.path.join(target_folder, filename)

                    # 5. COLLISION DETECTION
                    if os.path.exists(final_destination):
                        msg = f"{datetime.now()},⚠️ SKIP,{filename},{folder_name},File already exists\n"
                        print(f"⚠️  SKIP: {filename}")
                        report.write(msg)
                        continue

                    # 6. MOVE THE FILE
                    shutil.move(file_path, final_destination)
                    msg = f"{datetime.now()},✅ MOVED,{filename},{folder_name},Success\n"
                    print(f"✅ Moved: {filename}")
                    report.write(msg)
                    moved_count += 1

                except PermissionError:
                    msg = f"{datetime.now()},❌ ERROR,{filename},None,File in use\n"
                    print(f"❌ ERROR: {filename} is in use.")
                    report.write(msg)
                except Exception as e:
                    clean_error = str(e).replace(',', ';')
                    msg = f"{datetime.now()},❌ ERROR,{filename},None,{clean_error}\n"
                    print(f"❌ ERROR: {clean_error}")
                    report.write(msg)

        # 7. FINAL SUMMARY (Restored original feedback logic)
        summary_line = f"✨ Task Complete! {moved_count} files moved."
        report.write(f"{datetime.now()},🏁 FINISH,None,None,{summary_line}\n")
        print(f"\n{summary_line}")

        notification.notify(
            title='Chronos Pipeline',
            message=f'Success! {moved_count} files organized.',  # <--- Updated
            timeout=5
        )


if __name__ == "__main__":
    run_organizer()