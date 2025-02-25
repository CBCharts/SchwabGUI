import os
import sys
from pathlib import Path
from datetime import datetime

# --------------------------- CONFIG --------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Moves up to 'project' folder
HISTORICAL_PATHS = [
    PROJECT_ROOT / "outputs" / "historical",
    PROJECT_ROOT / "outputs" / "NDX historical"
]

# Mapping user selection to number of folders to keep
RETENTION_MAP = {
    "Keep 2 Days": 2,
    "Keep 1 Week": 5,
    "Keep 1 Month": 30
}

# --------------------------- FUNCTIONS --------------------------- #
def get_folders_sorted_by_date(directory: Path):
    """Returns a list of folders with valid date formats sorted by newest first."""
    if not directory.exists() or not directory.is_dir():
        return []

    date_folders = []
    for folder in directory.iterdir():
        if folder.is_dir() and folder.name.isdigit():  # Ensure folder name is numeric
            try:
                folder_date = datetime.strptime(folder.name, "%Y%m%d")
                date_folders.append((folder, folder_date))
            except ValueError:
                continue  # Skip invalid folder names

    # Sort folders by date (newest first)
    date_folders.sort(key=lambda x: x[1], reverse=True)
    return date_folders


def delete_old_files(max_folders_to_keep: int):
    """Deletes all CSV and XLSX files in folders older than the N most recent folders."""
    for hist_path in HISTORICAL_PATHS:
        if not hist_path.exists():
            print(f"Skipping non-existent path: {hist_path}")
            continue

        folders = get_folders_sorted_by_date(hist_path)

        if len(folders) <= max_folders_to_keep:
            print(f"✅ Retaining all files. Only {len(folders)} folders exist.")
            continue  # Nothing to delete

        # Keep only the most recent N folders, delete files from the rest
        folders_to_delete = folders[max_folders_to_keep:]  # Keep the N most recent

        for folder, _ in folders_to_delete:
            files_to_delete = list(folder.glob("*.csv")) + list(folder.glob("*.xlsx"))  # 🔹 Targets both file types

            if not files_to_delete:
                print(f"📂 No CSV/XLSX files to delete in: {folder}")
                continue

            for file in files_to_delete:
                try:
                    file.unlink()  # Delete file
                    print(f"🗑️ Deleted: {file}")
                except Exception as e:
                    print(f"⚠️ Error deleting {file}: {e}")

# --------------------------- MAIN EXECUTION --------------------------- #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clear_hist.py '<Retention Option>'")
        sys.exit(1)

    user_choice = sys.argv[1]
    max_folders_to_keep = RETENTION_MAP.get(user_choice)

    if not max_folders_to_keep:
        print(f"Invalid option: {user_choice}")
        sys.exit(1)

    print(f"🔹 Keeping the {max_folders_to_keep} most recent folders.")
    delete_old_files(max_folders_to_keep)
    print("✅ CSV Cleanup complete!")
