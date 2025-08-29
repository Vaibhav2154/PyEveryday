def dashboard_summary():
    tracker = TimeTracker()
    today = datetime.date.today().isoformat()
    today_acts = [a for a in tracker.activities if a.date == today]
    total_sec = sum(a.duration for a in today_acts)
    if not today_acts:
        return "No time tracked today."
    last = max(today_acts, key=lambda a: a.end_time or 0)
    h = int(total_sec // 3600)
    m = int((total_sec % 3600) // 60)
    msg = f"Total today: {h:02d}:{m:02d}"
    msg += f"\nLast: {last.name} ({last.category})"
    return msg
import time
import json
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import os

class Activity:
    def __init__(self, name, category="General"):
        self.name = name
        self.category = category
        self.start_time = None
        self.end_time = None
        self.duration = 0
        self.date = datetime.date.today().isoformat()
    
    def start(self):
        self.start_time = time.time()
        print(f"Started tracking: {self.name}")
    
    def stop(self):
        if self.start_time:
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time
            print(f"Stopped tracking: {self.name}")
            print(f"Duration: {self.format_duration(self.duration)}")
            return self.duration
        return 0
    
    def format_duration(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        activity = cls(data['name'], data['category'])
        activity.start_time = data['start_time']
        activity.end_time = data['end_time']
        activity.duration = data['duration']
        activity.date = data['date']
        return activity

class TimeTracker:
    def __init__(self, filename="time_tracking.json"):
        self.filename = filename
        self.activities = self.load_activities()
        self.current_activity = None
    
    def load_activities(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Activity.from_dict(item) for item in data]
        return []
    
    def save_activities(self):
        with open(self.filename, 'w') as f:
            json.dump([activity.to_dict() for activity in self.activities], f, indent=2)
    
    def start_activity(self, name, category="General"):
        if self.current_activity:
            print(f"Stopping current activity: {self.current_activity.name}")
            self.stop_current_activity()
        
        self.current_activity = Activity(name, category)
        self.current_activity.start()
    
    def stop_current_activity(self):
        if self.current_activity:
            duration = self.current_activity.stop()
            if duration > 0:
                self.activities.append(self.current_activity)
                self.save_activities()
            self.current_activity = None
            return duration
        else:
            print("No activity currently being tracked")
            return 0
    
    def get_daily_summary(self, date=None):
        if date is None:
            date = datetime.date.today().isoformat()
        
        daily_activities = [a for a in self.activities if a.date == date]
        
        if not daily_activities:
            print(f"No activities tracked for {date}")
            return
        
        total_time = sum(a.duration for a in daily_activities)
        category_time = defaultdict(float)
        
        print(f"\nDaily Summary for {date}")
        print("="*40)
        
        for activity in daily_activities:
            category_time[activity.category] += activity.duration
            print(f"{activity.name} ({activity.category}): {activity.format_duration(activity.duration)}")
        
        print("\nCategory Summary:")
        for category, duration in category_time.items():
            percentage = (duration / total_time) * 100 if total_time > 0 else 0
            print(f"{category}: {Activity('', '').format_duration(duration)} ({percentage:.1f}%)")
        
        print(f"\nTotal Time Tracked: {Activity('', '').format_duration(total_time)}")
    
    def get_weekly_summary(self):
        today = datetime.date.today()
        week_start = today - datetime.timedelta(days=today.weekday())
        
        weekly_activities = []
        for i in range(7):
            day = (week_start + datetime.timedelta(days=i)).isoformat()
            daily_activities = [a for a in self.activities if a.date == day]
            weekly_activities.extend(daily_activities)
        
        if not weekly_activities:
            print("No activities tracked this week")
            return
        
        category_time = defaultdict(float)
        daily_time = defaultdict(float)
        
        for activity in weekly_activities:
            category_time[activity.category] += activity.duration
            daily_time[activity.date] += activity.duration
        
        print("\nWeekly Summary")
        print("="*40)
        
        print("Daily Totals:")
        for i in range(7):
            day = (week_start + datetime.timedelta(days=i)).isoformat()
            day_name = (week_start + datetime.timedelta(days=i)).strftime("%A")
            duration = daily_time.get(day, 0)
            print(f"{day_name}: {Activity('', '').format_duration(duration)}")
        
        print("\nCategory Totals:")
        total_time = sum(category_time.values())
        for category, duration in category_time.items():
            percentage = (duration / total_time) * 100 if total_time > 0 else 0
            print(f"{category}: {Activity('', '').format_duration(duration)} ({percentage:.1f}%)")
    
    def generate_report(self, days=7):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days-1)
        
        activities_in_range = [
            a for a in self.activities 
            if start_date.isoformat() <= a.date <= end_date.isoformat()
        ]
        
        if not activities_in_range:
            print(f"No activities in the last {days} days")
            return
        
        category_data = defaultdict(float)
        daily_data = defaultdict(float)
        
        for activity in activities_in_range:
            category_data[activity.category] += activity.duration / 3600
            daily_data[activity.date] += activity.duration / 3600
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            categories = list(category_data.keys())
            times = list(category_data.values())
            ax1.pie(times, labels=categories, autopct='%1.1f%%')
            ax1.set_title('Time Distribution by Category')
            
            dates = sorted(daily_data.keys())
            daily_times = [daily_data[date] for date in dates]
            ax2.bar(dates, daily_times)
            ax2.set_title('Daily Time Tracking')
            ax2.set_ylabel('Hours')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig(f'time_report_{end_date}.png')
            print(f"Report saved as time_report_{end_date}.png")
            
        except Exception as e:
            print(f"Could not generate chart: {e}")
            print("Text report:")
            for category, hours in category_data.items():
                print(f"{category}: {hours:.2f} hours")
    
    def list_categories(self):
        categories = set(a.category for a in self.activities)
        if categories:
            print("Available categories:")
            for category in sorted(categories):
                print(f"- {category}")
        else:
            print("No categories found")


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Time Tracker")
    parser.add_argument('--start', nargs='+', metavar=('ACTIVITY', 'CATEGORY'), help='Start a new activity. Usage: --start <activity> [category]')
    parser.add_argument('--stop', action='store_true', help='Stop the current activity')
    parser.add_argument('--summary', nargs='?', const='', metavar='DATE', help='Show daily summary for DATE (YYYY-MM-DD), or today if not provided')
    parser.add_argument('--weekly', action='store_true', help='Show weekly summary')
    parser.add_argument('--report', type=int, metavar='DAYS', help='Generate report for the last DAYS (default 7)')
    parser.add_argument('--categories', action='store_true', help='List all categories')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    args = parser.parse_args()

    tracker = TimeTracker()

    if args.start:
        name = args.start[0]
        category = args.start[1] if len(args.start) > 1 else "General"
        tracker.start_activity(name, category)
    elif args.stop:
        tracker.stop_current_activity()
    elif args.summary is not None:
        date = args.summary if args.summary else None
        tracker.get_daily_summary(date)
    elif args.weekly:
        tracker.get_weekly_summary()
    elif args.report is not None:
        tracker.generate_report(args.report)
    elif args.categories:
        tracker.list_categories()
    elif args.interactive or len(sys.argv) == 1:
        print("Usage: python time_tracker.py --start ACTIVITY [CATEGORY] | --stop | --summary [DATE] | --weekly | --report DAYS | --categories | --interactive")
