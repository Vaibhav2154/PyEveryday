def dashboard_summary():
    # Show completed sessions today
    try:
        stats_file = "pomodoro_stats.json"
        import json, datetime
        today = datetime.date.today().isoformat()
        if not os.path.exists(stats_file):
            return "No pomodoro sessions yet."
        with open(stats_file, 'r') as f:
            data = json.load(f)
        today_sessions = [s for s in data if s.get('date') == today]
        return f"Sessions today: {len(today_sessions)}"
    except Exception:
        return "No pomodoro stats available."

import time
import datetime
import sys
import threading
import os
import argparse

class PomodoroTimer:
    def __init__(self, work_duration=25, break_duration=5, long_break_duration=15):
        self.work_duration = work_duration * 60
        self.break_duration = break_duration * 60
        self.long_break_duration = long_break_duration * 60
        self.sessions_completed = 0
        self.current_session = None
        self.timer_running = False
        self.paused = False
        self.remaining_time = 0
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def play_notification(self):
        try:
            if os.name == 'nt':
                import winsound
                winsound.Beep(1000, 1000)
            else:
                print('\a')
        except:
            print("🔔 Time's up!")
    
    def countdown(self, duration, session_type):
        self.timer_running = True
        self.remaining_time = duration
        
        print(f"\n{session_type} started - {self.format_time(duration)}")
        
        while self.remaining_time > 0 and self.timer_running:
            if not self.paused:
                print(f"\r{session_type}: {self.format_time(self.remaining_time)}", end="", flush=True)
                time.sleep(1)
                self.remaining_time -= 1
            else:
                time.sleep(0.1)
        
        if self.timer_running:
            print(f"\n{session_type} completed!")
            self.play_notification()
            
            if session_type == "Work Session":
                self.sessions_completed += 1
                print(f"Sessions completed: {self.sessions_completed}")
        
        self.timer_running = False
    
    def start_work_session(self):
        if not self.timer_running:
            self.current_session = "work"
            thread = threading.Thread(target=self.countdown, args=(self.work_duration, "Work Session"))
            thread.daemon = True
            thread.start()
            return thread
        else:
            print("Timer is already running")
    
    def start_break(self):
        if not self.timer_running:
            break_duration = self.long_break_duration if self.sessions_completed % 4 == 0 and self.sessions_completed > 0 else self.break_duration
            break_type = "Long Break" if break_duration == self.long_break_duration else "Short Break"
            self.current_session = "break"
            thread = threading.Thread(target=self.countdown, args=(break_duration, break_type))
            thread.daemon = True
            thread.start()
            return thread
        else:
            print("Timer is already running")
    
    def pause(self):
        if self.timer_running:
            self.paused = not self.paused
            status = "paused" if self.paused else "resumed"
            print(f"\nTimer {status}")
        else:
            print("No timer running")
    
    def stop(self):
        if self.timer_running:
            self.timer_running = False
            print("\nTimer stopped")
        else:
            print("No timer running")
    
    def reset_sessions(self):
        self.sessions_completed = 0
        print("Session count reset")
    
    def get_stats(self):
        total_work_time = self.sessions_completed * (self.work_duration // 60)
        print(f"\nPomodoro Statistics:")
        print(f"Sessions completed: {self.sessions_completed}")
        print(f"Total work time: {total_work_time} minutes")
        print(f"Next break type: {'Long' if self.sessions_completed % 4 == 0 and self.sessions_completed > 0 else 'Short'}")

def interactive_mode():
    timer = PomodoroTimer()
    print("Pomodoro Timer Started!")
    print("Commands: work, break, pause, stop, stats, reset, quit")
    
    while True:
        command = input("\nEnter command: ").strip().lower()
        
        if command == "work":
            thread = timer.start_work_session()
            if thread:
                try:
                    thread.join()
                except KeyboardInterrupt:
                    timer.stop()
        
        elif command == "break":
            thread = timer.start_break()
            if thread:
                try:
                    thread.join()
                except KeyboardInterrupt:
                    timer.stop()
        
        elif command == "pause":
            timer.pause()
        
        elif command == "stop":
            timer.stop()
        
        elif command == "stats":
            timer.get_stats()
        
        elif command == "reset":
            timer.reset_sessions()
        
        elif command == "quit":
            timer.stop()
            print("Goodbye!")
            break
        
        else:
            print("Unknown command")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pomodoro Timer")
    parser.add_argument('--work', type=int, help='Work session duration in minutes')
    parser.add_argument('--break', dest='break_', type=int, help='Short break duration in minutes')
    parser.add_argument('--long-break', type=int, help='Long break duration in minutes')
    parser.add_argument('--session', choices=['work', 'break'], help='Start a work or break session immediately')
    parser.add_argument('--stats', action='store_true', help='Show Pomodoro statistics')
    parser.add_argument('--reset', action='store_true', help='Reset session count')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    args = parser.parse_args()

    # If any CLI flag is used, run in CLI mode
    if any([args.work, args.break_, args.long_break, args.session, args.stats, args.reset]) and not args.interactive:
        timer = PomodoroTimer(
            work_duration=args.work if args.work else 25,
            break_duration=args.break_ if args.break_ else 5,
            long_break_duration=args.long_break if args.long_break else 15
        )
        if args.session == 'work':
            thread = timer.start_work_session()
            if thread:
                try:
                    thread.join()
                except KeyboardInterrupt:
                    timer.stop()
        elif args.session == 'break':
            thread = timer.start_break()
            if thread:
                try:
                    thread.join()
                except KeyboardInterrupt:
                    timer.stop()
        if args.stats:
            timer.get_stats()
        if args.reset:
            timer.reset_sessions()
    else:
        interactive_mode()
