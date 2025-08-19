import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderMonitor(FileSystemEventHandler):
    def __init__(self, action_script=None):
        self.action_script = action_script
    
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            if self.action_script:
                self.execute_action(event.src_path, "modified")
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            if self.action_script:
                self.execute_action(event.src_path, "created")
    
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            if self.action_script:
                self.execute_action(event.src_path, "deleted")
    
    def on_moved(self, event):
        if not event.is_directory:
            print(f"File moved: {event.src_path} -> {event.dest_path}")
            if self.action_script:
                self.execute_action(event.dest_path, "moved")
    
    def execute_action(self, file_path, action):
        try:
            subprocess.run([sys.executable, self.action_script, file_path, action], 
                         check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing action script: {e}")

def monitor_folder(folder_path, action_script=None):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist")
        return
    
    event_handler = FolderMonitor(action_script)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    
    observer.start()
    print(f"Monitoring folder: {folder_path}")
    print("Press Ctrl+C to stop monitoring...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped")
    
    observer.join()

def create_sample_action_script():
    sample_script = '''import sys
import shutil
import os

file_path = sys.argv[1]
action = sys.argv[2]

if action == "created" and file_path.endswith('.txt'):
    backup_dir = "backup_texts"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, filename)
    shutil.copy2(file_path, backup_path)
    print(f"Backed up {filename} to {backup_dir}")
'''
    
    with open('sample_action.py', 'w') as f:
        f.write(sample_script)
    print("Sample action script created: sample_action.py")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python folder_monitor.py <folder_path> [action_script]")
        print("Use 'create_sample' to create a sample action script")
        sys.exit(1)
    
    if sys.argv[1] == "create_sample":
        create_sample_action_script()
        sys.exit(0)
    
    folder_path = sys.argv[1]
    action_script = sys.argv[2] if len(sys.argv) > 2 else None
    
    monitor_folder(folder_path, action_script)
