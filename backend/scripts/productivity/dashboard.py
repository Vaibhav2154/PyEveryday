"""
PyEveryday Daily Dashboard

This script provides a centralized dashboard for productivity tools:
 - Todos
 - Reminders
 - Pomodoro Timer
 - Time Tracking
 - Weather
 - Motivational Quote
 - Configurable section toggles
"""

import os
import json
try:
	from quote_fetcher import QuoteFetcher
except ImportError:
	try:
		from productivity.quote_fetcher import QuoteFetcher
	except ImportError:
		try:
			from backend.scripts.productivity.quote_fetcher import QuoteFetcher
		except ImportError:
			QuoteFetcher = None
from datetime import datetime
import requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'dashboard_config.json')
DEFAULT_CONFIG = {
	"show_todos": True,
	"show_reminders": True,
	"show_pomodoro": True,
	"show_time_tracking": True,
	"show_quote": True,
	# Weather removed
}

def load_config():
	if os.path.exists(CONFIG_PATH):
		try:
			with open(CONFIG_PATH, 'r') as f:
				return json.load(f)
		except Exception:
			pass
	return DEFAULT_CONFIG.copy()

config = load_config()

def section_header(title):
	return f"\n--- {title} ---"



# --- Motivational Quote ---
def get_motivational_quote():
	if QuoteFetcher is None:
		return "Quote: (not available)"
	try:
		fetcher = QuoteFetcher()
		return fetcher.get_local_quote()
	except Exception as e:
		return f"Quote: ERROR: {type(e).__name__}: {e}"

# --- Dynamic Section Loader ---
def try_import_and_run(module_name, func_name, section_title):
	try:
		import importlib
		mod = importlib.import_module(module_name)
		func = getattr(mod, func_name)
		result = func()
		if result:
			return section_header(section_title) + f"\n{result}"
	except Exception as e:
		return section_header(section_title) + f"\nERROR: {type(e).__name__}: {e}"
	return ""

def main():
	print("\n=== PyEveryday Daily Dashboard ===\n")
	print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

	# Todos
	if config.get("show_todos", True):
		print(try_import_and_run('todo_manager', 'dashboard_summary', 'Todos'))

	# Reminders
	if config.get("show_reminders", True):
		print(try_import_and_run('reminder_system', 'dashboard_summary', 'Reminders'))

	# Pomodoro
	if config.get("show_pomodoro", True):
		print(try_import_and_run('pomodoro_timer', 'dashboard_summary', 'Pomodoro Timer'))

	# Time Tracking
	if config.get("show_time_tracking", True):
		print(try_import_and_run('time_tracker', 'dashboard_summary', 'Time Tracking'))



	# Motivational Quote
	if config.get("show_quote", True):
		print(section_header('Motivational Quote'))
		print(get_motivational_quote())

if __name__ == "__main__":
	main()
