#!/usr/bin/env python3
"""
GoAmrita - Setup Windows Task Scheduler v1.0
=============================================
Creates Windows Scheduled Tasks for all GoAmrita automation.

Tasks created:
  1. Daily Pipeline     — 8:30 AM daily
  2. Sales Compare      — Every 2 hours
  3. Buy Box Monitor    — Every 2 hours
  4. Stock Monitor      — Every 2 hours
  5. Campaign Creator   — Every 15 days (top profit)

Each task runs the central scheduler with specific command.

Usage:
    python setup_windows_scheduler.py --create    (create all tasks)
    python setup_windows_scheduler.py --list      (show status)
    python setup_windows_scheduler.py --delete    (remove all tasks)
"""

import os
import sys
import subprocess
import argparse

PYTHON = r"C:\Users\Clu\AppData\Local\Programs\Python\Python311\python.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_dir(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if os.path.exists(os.path.join(current, "config_features.json")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for Windows scheduler setup")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SCHEDULER = os.path.join(PROJECT_DIR, "Grow24_AI", "core", "orchestrator", "scheduler_v1.0.py")

TASKS = [
    {
        "name": "GoAmrita_DailyPipeline",
        "description": "GoAmrita Daily Pipeline — Import, Analyze, Report",
        "command": f'"{PYTHON}" "{SCHEDULER}" --run daily',
        "schedule": "/sc DAILY /st 08:30",
    },
    {
        "name": "GoAmrita_SalesCompare",
        "description": "GoAmrita Sales Compare — Every 2 hours",
        "command": f'"{PYTHON}" "{os.path.join(SCRIPT_DIR, "intraday_sales_v1.0.py")}"',
        "schedule": "/sc HOURLY /mo 2 /st 08:17",
    },
    {
        "name": "GoAmrita_BuyBoxMonitor",
        "description": "GoAmrita Buy Box Monitor — Every 2 hours",
        "command": f'"{PYTHON}" "{os.path.join(PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "market_intelligence", "buy_box_monitor_v1.1.py")}"',
        "schedule": "/sc HOURLY /mo 2 /st 08:43",
    },
    {
        "name": "GoAmrita_StockMonitor",
        "description": "GoAmrita Stock Monitor — Every 2 hours",
        "command": f'"{PYTHON}" "{os.path.join(PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "inventory", "stock_monitor_v1.1.py")}"',
        "schedule": "/sc HOURLY /mo 2 /st 09:07",
    },
    {
        "name": "GoAmrita_CampaignCreator",
        "description": "GoAmrita Auto Campaign — New Listings Daily",
        "command": f'"{PYTHON}" "{os.path.join(SCRIPT_DIR, "auto_campaign_creator_v2.0.py")}" --mode newlisting --days 8',
        "schedule": "/sc DAILY /st 09:00",
    },
]


def create_tasks():
    print("Creating Windows Scheduled Tasks...\n")
    for task in TASKS:
        cmd = (
            f'schtasks /create /tn "{task["name"]}" '
            f'/tr "{task["command"]}" '
            f'{task["schedule"]} '
            f'/f '
            f'/rl HIGHEST '
            f'/ru "{os.environ.get("USERNAME", "Clu")}"'
        )
        print(f"  {task['name']}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    Created!")
        else:
            print(f"    Error: {result.stderr.strip()[:100]}")

    print(f"\nAll tasks created! Check with: schtasks /query /fo TABLE | findstr GoAmrita")


def list_tasks():
    print("GoAmrita Scheduled Tasks:\n")
    result = subprocess.run(
        'schtasks /query /fo TABLE /nh', shell=True, capture_output=True, text=True
    )
    for line in result.stdout.split('\n'):
        if 'GoAmrita' in line:
            print(f"  {line.strip()}")

    if 'GoAmrita' not in result.stdout:
        print("  No GoAmrita tasks found. Run --create first.")


def delete_tasks():
    print("Deleting GoAmrita tasks...\n")
    for task in TASKS:
        cmd = f'schtasks /delete /tn "{task["name"]}" /f'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Deleted: {task['name']}")
        else:
            print(f"  Not found: {task['name']}")


def main():
    parser = argparse.ArgumentParser(description='Setup Windows Scheduler')
    parser.add_argument('--create', action='store_true', help='Create all scheduled tasks')
    parser.add_argument('--list', action='store_true', help='List current tasks')
    parser.add_argument('--delete', action='store_true', help='Delete all tasks')
    args = parser.parse_args()

    print("=" * 55)
    print("  GoAmrita — Windows Task Scheduler Setup")
    print("=" * 55)

    if args.create:
        create_tasks()
    elif args.list:
        list_tasks()
    elif args.delete:
        delete_tasks()
    else:
        parser.print_help()
        print("\nTasks that will be created:")
        for t in TASKS:
            print(f"  {t['name']:<35} {t['schedule'].split('/st')[0].strip()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
