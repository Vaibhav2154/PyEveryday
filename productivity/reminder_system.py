import datetime
import time
import json
import threading
import os

class Reminder:
    def __init__(self, message, reminder_time, repeat=False, repeat_interval=None):
        self.message = message
        self.reminder_time = reminder_time
        self.repeat = repeat
        self.repeat_interval = repeat_interval
        self.active = True
        self.id = str(int(time.time() * 1000))
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'reminder_time': self.reminder_time.isoformat(),
            'repeat': self.repeat,
            'repeat_interval': self.repeat_interval,
            'active': self.active
        }
    
    @classmethod
    def from_dict(cls, data):
        reminder = cls(
            data['message'],
            datetime.datetime.fromisoformat(data['reminder_time']),
            data['repeat'],
            data['repeat_interval']
        )
        reminder.id = data['id']
        reminder.active = data['active']
        return reminder

class ReminderManager:
    def __init__(self, filename="reminders.json"):
        self.filename = filename
        self.reminders = self.load_reminders()
        self.running = False
    
    def load_reminders(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Reminder.from_dict(item) for item in data]
        return []
    
    def save_reminders(self):
        with open(self.filename, 'w') as f:
            json.dump([reminder.to_dict() for reminder in self.reminders], f, indent=2)
    
    def add_reminder(self, message, reminder_time, repeat=False, repeat_interval=None):
        reminder = Reminder(message, reminder_time, repeat, repeat_interval)
        self.reminders.append(reminder)
        self.save_reminders()
        print(f"Reminder added: {message} at {reminder_time}")
        return reminder.id
    
    def remove_reminder(self, reminder_id):
        self.reminders = [r for r in self.reminders if r.id != reminder_id]
        self.save_reminders()
        print(f"Reminder {reminder_id} removed")
    
    def list_reminders(self):
        if not self.reminders:
            print("No reminders found")
            return
        
        active_reminders = [r for r in self.reminders if r.active]
        if not active_reminders:
            print("No active reminders")
            return
        
        print("\nActive Reminders:")
        for reminder in active_reminders:
            repeat_str = f" (Repeats every {reminder.repeat_interval})" if reminder.repeat else ""
            print(f"ID: {reminder.id}")
            print(f"Message: {reminder.message}")
            print(f"Time: {reminder.reminder_time}{repeat_str}")
            print("-" * 40)
    
    def trigger_reminder(self, reminder):
        print(f"\n🔔 REMINDER: {reminder.message}")
        print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            if os.name == 'nt':
                import winsound
                winsound.Beep(800, 500)
            else:
                print('\a')
        except:
            pass
        
        if reminder.repeat and reminder.repeat_interval:
            next_time = self.calculate_next_time(reminder.reminder_time, reminder.repeat_interval)
            reminder.reminder_time = next_time
            print(f"Next reminder: {next_time}")
        else:
            reminder.active = False
        
        self.save_reminders()
    
    def calculate_next_time(self, current_time, interval):
        if interval.endswith('m'):
            minutes = int(interval[:-1])
            return current_time + datetime.timedelta(minutes=minutes)
        elif interval.endswith('h'):
            hours = int(interval[:-1])
            return current_time + datetime.timedelta(hours=hours)
        elif interval.endswith('d'):
            days = int(interval[:-1])
            return current_time + datetime.timedelta(days=days)
        else:
            return current_time + datetime.timedelta(hours=1)
    
    def check_reminders(self):
        now = datetime.datetime.now()
        for reminder in self.reminders:
            if reminder.active and reminder.reminder_time <= now:
                self.trigger_reminder(reminder)
    
    def start_monitoring(self):
        self.running = True
        print("Reminder monitoring started. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                self.check_reminders()
                time.sleep(30)
        except KeyboardInterrupt:
            self.running = False
            print("\nReminder monitoring stopped")
    
    def parse_time_string(self, time_str):
        try:
            if 'T' in time_str:
                return datetime.datetime.fromisoformat(time_str)
            else:
                today = datetime.date.today()
                time_part = datetime.datetime.strptime(time_str, '%H:%M').time()
                reminder_datetime = datetime.datetime.combine(today, time_part)
                
                if reminder_datetime < datetime.datetime.now():
                    reminder_datetime += datetime.timedelta(days=1)
                
                return reminder_datetime
        except ValueError:
            return None

def create_quick_reminders():
    manager = ReminderManager()
    
    quick_reminders = [
        ("Take a break", datetime.datetime.now() + datetime.timedelta(hours=1)),
        ("Drink water", datetime.datetime.now() + datetime.timedelta(minutes=30), True, "30m"),
        ("Check emails", datetime.datetime.now() + datetime.timedelta(hours=2))
    ]
    
    for message, time, *args in quick_reminders:
        repeat = args[0] if len(args) > 0 else False
        interval = args[1] if len(args) > 1 else None
        manager.add_reminder(message, time, repeat, interval)
    
    print("Quick reminders created!")

if __name__ == "__main__":
    import sys
    
    manager = ReminderManager()
    
    if len(sys.argv) < 2:
        print("Usage: python reminder_system.py <command> [args]")
        print("Commands: add, list, remove, monitor, quick")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: add <message> <time> [repeat_interval]")
            print("Time format: HH:MM or YYYY-MM-DDTHH:MM")
            sys.exit(1)
        
        message = sys.argv[2]
        time_str = sys.argv[3]
        repeat_interval = sys.argv[4] if len(sys.argv) > 4 else None
        
        reminder_time = manager.parse_time_string(time_str)
        if reminder_time:
            repeat = repeat_interval is not None
            manager.add_reminder(message, reminder_time, repeat, repeat_interval)
        else:
            print("Invalid time format")
    
    elif command == "list":
        manager.list_reminders()
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: remove <reminder_id>")
            sys.exit(1)
        
        reminder_id = sys.argv[2]
        manager.remove_reminder(reminder_id)
    
    elif command == "monitor":
        manager.start_monitoring()
    
    elif command == "quick":
        create_quick_reminders()
    
    else:
        print("Unknown command")
