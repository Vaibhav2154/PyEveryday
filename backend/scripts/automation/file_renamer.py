import os
import sys

def rename_files(directory, old_pattern, new_pattern):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist")
        return
    
    files = os.listdir(directory)
    renamed_count = 0
    
    for filename in files:
        if old_pattern in filename:
            old_path = os.path.join(directory, filename)
            new_filename = filename.replace(old_pattern, new_pattern)
            new_path = os.path.join(directory, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming {filename}: {e}")
    
    print(f"Total files renamed: {renamed_count}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python file_renamer.py <directory> <old_pattern> <new_pattern>")
        sys.exit(1)
    
    directory = sys.argv[1]
    old_pattern = sys.argv[2]
    new_pattern = sys.argv[3]
    
    rename_files(directory, old_pattern, new_pattern)
