import os
import shutil
from pathlib import Path

def organize_files_by_extension(source_dir):
    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} does not exist")
        return
    
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        if os.path.isfile(file_path):
            file_extension = Path(filename).suffix.lower()
            
            if not file_extension:
                file_extension = "no_extension"
            else:
                file_extension = file_extension[1:]
            
            dest_dir = os.path.join(source_dir, file_extension)
            
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved {filename} to {file_extension}/")
            except Exception as e:
                print(f"Error moving {filename}: {e}")

def organize_files_by_date(source_dir):
    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} does not exist")
        return
    
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            creation_time = stat.st_ctime
            
            import datetime
            date = datetime.datetime.fromtimestamp(creation_time)
            year_month = date.strftime("%Y-%m")
            
            dest_dir = os.path.join(source_dir, year_month)
            
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved {filename} to {year_month}/")
            except Exception as e:
                print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python file_organizer.py <directory> <type>")
        print("Types: extension, date")
        sys.exit(1)
    
    directory = sys.argv[1]
    org_type = sys.argv[2]
    
    if org_type == "extension":
        organize_files_by_extension(directory)
    elif org_type == "date":
        organize_files_by_date(directory)
    else:
        print("Invalid type. Use 'extension' or 'date'")
