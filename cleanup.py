import os
import shutil

def delete_pycache_and_logs(root_dir="."):
    """Deletes all __pycache__ folders and .log files in the given directory."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove __pycache__ folders
        if "__pycache__" in dirnames:
            cache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(cache_path)
            print(f"Deleted: {cache_path}")

        # Remove .log files
        for filename in filenames:
            if filename.endswith(".log"):
                log_path = os.path.join(dirpath, filename)
                os.remove(log_path)
                print(f"Deleted: {log_path}")

if __name__ == "__main__":
    project_root = os.path.abspath(".")  # Change this if running from another location
    delete_pycache_and_logs(project_root)
    print("\n✅ Cleanup complete!")
