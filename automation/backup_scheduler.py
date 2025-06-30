import os
import schedule
import time
import shutil
import datetime
import zipfile

def backup_directory(source_dir, backup_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist")
        return False
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    try:
        shutil.copytree(source_dir, backup_path)
        print(f"Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def backup_and_compress(source_dir, backup_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist")
        return False
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(backup_dir, zip_name)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Compressed backup created: {zip_path}")
        return True
    except Exception as e:
        print(f"Backup compression failed: {e}")
        return False

def cleanup_old_backups(backup_dir, days_to_keep=7):
    if not os.path.exists(backup_dir):
        return
    
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.getmtime(item_path) < cutoff_time:
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                print(f"Removed old backup: {item}")
            except Exception as e:
                print(f"Error removing {item}: {e}")

def scheduled_backup(source_dir, backup_dir, compress=True):
    print(f"Starting scheduled backup at {datetime.datetime.now()}")
    
    if compress:
        success = backup_and_compress(source_dir, backup_dir)
    else:
        success = backup_directory(source_dir, backup_dir)
    
    if success:
        cleanup_old_backups(backup_dir)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python backup_scheduler.py <source_dir> <backup_dir> [schedule_type]")
        print("Schedule types: daily, hourly, manual")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    backup_dir = sys.argv[2]
    schedule_type = sys.argv[3] if len(sys.argv) > 3 else "manual"
    
    if schedule_type == "daily":
        schedule.every().day.at("02:00").do(scheduled_backup, source_dir, backup_dir)
        print("Daily backup scheduled at 2:00 AM")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif schedule_type == "hourly":
        schedule.every().hour.do(scheduled_backup, source_dir, backup_dir)
        print("Hourly backup scheduled")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        scheduled_backup(source_dir, backup_dir)
