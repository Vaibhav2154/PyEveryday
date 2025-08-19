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
    import sys
    
    manager = TodoManager()
    
    if len(sys.argv) < 2:
        print("Usage: python todo_manager.py <command> [args]")
        print("Commands: add, list, complete, remove, today")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: add <task> [priority] [due_date]")
            sys.exit(1)
        
        task = sys.argv[2]
        priority = Priority[sys.argv[3].upper()] if len(sys.argv) > 3 else Priority.MEDIUM
        due_date = sys.argv[4] if len(sys.argv) > 4 else None
        
        manager.add_task(task, priority, due_date)
    
    elif command == "list":
        show_completed = len(sys.argv) > 2 and sys.argv[2] == "all"
        manager.list_tasks(show_completed)
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: complete <index>")
            sys.exit(1)
        
        index = int(sys.argv[2])
        manager.complete_task(index)
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: remove <index>")
            sys.exit(1)
        
        index = int(sys.argv[2])
        manager.remove_task(index)
    
    elif command == "today":
        today_tasks = manager.get_today_tasks()
        if today_tasks:
            print("Today's tasks:")
            for i, task in enumerate(today_tasks):
                print(f"{i}: {task.task}")
        else:
            print("No tasks due today")
    
    else:
        print("Unknown command")
