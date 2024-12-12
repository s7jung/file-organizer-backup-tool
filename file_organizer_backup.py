import os
import shutil
import zipfile
from datetime import datetime

def organize_files_by_date_and_extension(src_folder):
    """Organizes files in the source folder by date and extension."""
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get file's modification date and extension
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            date_folder = mod_time.strftime("%Y-%m-%d")
            ext = os.path.splitext(file)[1][1:]  # remove the dot
            
            # Create target folder structure
            target_folder = os.path.join(src_folder, date_folder, ext or "no_extension")
            os.makedirs(target_folder, exist_ok=True)

            # Move file to the target folder
            shutil.move(file_path, os.path.join(target_folder, file))

def backup_to_external(target_folder, backup_location):
    """Backs up the target folder to an external location."""
    if os.path.exists(backup_location):
        backup_path = shutil.copytree(target_folder, backup_location, dirs_exist_ok=True)
        print(f"Backup completed at: {backup_path}")
    else:
        print(f"Backup location not found: {backup_location}")

def compress_old_files(src_folder, days_old):
    """Compresses files older than a specified number of days into a zip file."""
    cutoff_date = datetime.now().timestamp() - (days_old * 86400)
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_date:
                zip_name = os.path.join(root, f"archived_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
                with zipfile.ZipFile(zip_name, 'a') as zipf:
                    zipf.write(file_path, os.path.relpath(file_path, src_folder))
                os.remove(file_path)
                print(f"Compressed and removed: {file_path}")

def main():
    src_folder = input("Enter the source folder to organize: ").strip()
    backup_location = input("Enter the backup location: ").strip()
    days_old = int(input("Enter the number of days after which files should be compressed: "))

    if not os.path.exists(src_folder):
        print(f"Source folder not found: {src_folder}")
        return

    print("Organizing files...")
    organize_files_by_date_and_extension(src_folder)

    print("Backing up files...")
    backup_to_external(src_folder, backup_location)

    print("Compressing old files...")
    compress_old_files(src_folder, days_old)

    print("Operation completed successfully!")

if __name__ == "__main__":
    main()
