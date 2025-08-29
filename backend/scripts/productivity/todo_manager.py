def dashboard_summary():
    mgr = TodoManager()
    total = len(mgr.todos)
    pending = [t for t in mgr.todos if not t.completed]
    if not mgr.todos:
        return "No todos."
    msg = f"Total: {total}, Pending: {len(pending)}"
    next_due = min((t for t in pending if t.due_date), key=lambda t: t.due_date, default=None)
    if next_due:
        msg += f"\nNext due: {next_due.task} (by {next_due.due_date})"
    return msg
import json
import os
import datetime
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoItem:
    def __init__(self, task, priority=Priority.MEDIUM, due_date=None):
        self.task = task
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'task': self.task,
            'priority': self.priority.value,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        item = cls(data['task'], Priority(data['priority']), data['due_date'])
        item.completed = data['completed']
        item.created_at = data['created_at']
        return item

class TodoManager:
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [TodoItem.from_dict(item) for item in data]
        return []
    
    def save_todos(self):
        with open(self.filename, 'w') as f:
            json.dump([todo.to_dict() for todo in self.todos], f, indent=2)
    
    def add_task(self, task, priority=Priority.MEDIUM, due_date=None):
        todo = TodoItem(task, priority, due_date)
        self.todos.append(todo)
        self.save_todos()
        print(f"Added task: {task}")
    
    def complete_task(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index].completed = True
            self.save_todos()
            print(f"Completed task: {self.todos[index].task}")
        else:
            print("Invalid task index")
    
    def remove_task(self, index):
        if 0 <= index < len(self.todos):
            removed = self.todos.pop(index)
            self.save_todos()
            print(f"Removed task: {removed.task}")
        else:
            print("Invalid task index")
    
    def list_tasks(self, show_completed=False):
        if not self.todos:
            print("No tasks found")
            return
        
        for i, todo in enumerate(self.todos):
            if not show_completed and todo.completed:
                continue
            
            status = "✓" if todo.completed else "○"
            priority_str = f"[{todo.priority.name}]"
            due_str = f" (Due: {todo.due_date})" if todo.due_date else ""
            
            print(f"{i}: {status} {priority_str} {todo.task}{due_str}")
    
    def get_today_tasks(self):
        today = datetime.date.today().isoformat()
        today_tasks = [todo for todo in self.todos if todo.due_date == today and not todo.completed]
        return today_tasks


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Todo Manager")
    parser.add_argument('--add', nargs='+', help='Add a new task. Usage: --add <task> [priority] [due_date]')
    parser.add_argument('--priority', choices=['LOW', 'MEDIUM', 'HIGH'], help='Priority for the new task')
    parser.add_argument('--due', help='Due date for the new task (YYYY-MM-DD)')
    parser.add_argument('--list', action='store_true', help='List all pending tasks')
    parser.add_argument('--list-all', action='store_true', help='List all tasks including completed')
    parser.add_argument('--complete', type=int, help='Mark a task as completed by index')
    parser.add_argument('--remove', type=int, help='Remove a task by index')
    parser.add_argument('--today', action='store_true', help="Show today's tasks")
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    args = parser.parse_args()

    manager = TodoManager()

    if args.add:
        task = ' '.join(args.add)
        priority = Priority[args.priority.upper()] if args.priority else Priority.MEDIUM
        due_date = args.due if args.due else None
        manager.add_task(task, priority, due_date)
    elif args.list:
        manager.list_tasks(show_completed=False)
    elif args.list_all:
        manager.list_tasks(show_completed=True)
    elif args.complete is not None:
        manager.complete_task(args.complete)
    elif args.remove is not None:
        manager.remove_task(args.remove)
    elif args.today:
        today_tasks = manager.get_today_tasks()
        if today_tasks:
            print("Today's tasks:")
            for i, task in enumerate(today_tasks):
                print(f"{i}: {task.task}")
        else:
            print("No tasks due today")
    elif args.interactive or len(sys.argv) == 1:
        # Fallback to original prompt-based usage if no CLI args
        print("Usage: python todo_manager.py --add <task> [--priority PRIORITY] [--due YYYY-MM-DD] | --list | --list-all | --complete INDEX | --remove INDEX | --today | --interactive")
