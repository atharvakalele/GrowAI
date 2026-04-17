#!/usr/bin/env python3
"""
Grow24 AI - Smart Scheduler v1.1
=================================
Single daemon. Freshness-based. Missed-task catch-up. No duplicates.

HOW IT WORKS:
  - Every task has freshness_hours (e.g. 0.5 = run every 30 min, 24 = daily)
  - Daemon checks every 60 seconds: is task stale? -> run it ONCE
  - Laptop was off 6 hours? -> stale tasks detected on startup -> run ONCE each (not 12x)
  - Already running? -> skip (no duplicates)
  - Dependencies auto-resolve: if "profit" depends on "import" and import is stale, import runs first

SCHEDULE EXAMPLES (all via freshness_hours):
  0.5   = every 30 min  (price optimizer)
  2     = every 2 hours (buy box monitor)
  4     = every 4 hours (data import)
  12    = every 12 hours (pricing refresh)
  24    = daily          (reports, profit calc)
  360   = every 15 days  (campaign: top profit)

DAILY PIPELINE:
  Tasks with freshness_hours >= 24 only run AFTER daily_pipeline_time (e.g. 08:30)
  This prevents daily tasks from firing at 2 AM if laptop was on.

Usage:
    python scheduler_v1.1.py --daemon              (main mode: run continuously)
    python scheduler_v1.1.py --run daily            (full daily pipeline once)
    python scheduler_v1.1.py --run monitor          (all monitors once)
    python scheduler_v1.1.py --run task import      (single task)
    python scheduler_v1.1.py --run from report_ads  (from step, auto-deps)
    python scheduler_v1.1.py --status               (show task status)
    python scheduler_v1.1.py --catchup              (run all stale tasks once, then exit)

Changes from v1.0:
  - Smart catch-up on startup (missed tasks run ONCE, not N times)
  - Running-task lock (no duplicate concurrent runs)
  - Daily-gate: daily tasks wait for daily_pipeline_time
  - Unified loop (no separate daily/monitor tracking)
  - Better logging with timestamps
"""

import json
import os
import sys
import io
import time
import subprocess
import argparse
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_dir(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if os.path.exists(os.path.join(current, "config_scheduler.json")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for scheduler v1.1")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
PYTHON = sys.executable
LEGACY_PYTHON_DIR = os.path.join(PROJECT_DIR, "ClaudeCode", "Python")
LOG_FILE = os.path.join(PROJECT_DIR, "ClaudeCode", "scheduler_log.json")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config_scheduler.json")

# Tasks currently running (prevent duplicates)
_running = set()


# ============================================
# CONFIG & LOG
# ============================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding='utf-8') as f:
            return json.load(f)
    print(f"  [WARN] Config not found: {CONFIG_FILE}")
    return {"version": "1.0", "daily_pipeline_time": "08:30", "tasks": {}, "pipelines": {}}


def load_log():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"runs": {}}


def save_log(log):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


# ============================================
# FRESHNESS CHECK
# ============================================
def get_age_hours(task_id, log):
    """Get how many hours since last successful run. Returns None if never run."""
    last = log.get("runs", {}).get(task_id, {}).get("last_success")
    if not last:
        return None
    try:
        last_dt = datetime.fromisoformat(last)
        return (datetime.now() - last_dt).total_seconds() / 3600
    except Exception:
        return None


def is_fresh(task_id, config, log):
    """Check if task output is still fresh (don't need to re-run)"""
    task = config.get("tasks", {}).get(task_id, {})
    freshness_hours = task.get("freshness_hours", 4)
    age = get_age_hours(task_id, log)
    if age is None:
        return False  # never run
    return age < freshness_hours


# ============================================
# DAILY GATE
# ============================================
def passes_daily_gate(task_id, config):
    """Daily tasks (freshness >= 24h) only run after daily_pipeline_time.
    Sub-daily tasks (freshness < 24h) can run anytime."""
    task = config.get("tasks", {}).get(task_id, {})
    freshness = task.get("freshness_hours", 4)

    # Sub-daily tasks: always allowed
    if freshness < 24:
        return True

    # Daily+ tasks: only after pipeline time
    pipeline_time = config.get("daily_pipeline_time", "08:30")
    now_time = datetime.now().strftime("%H:%M")
    return now_time >= pipeline_time


# ============================================
# DEPENDENCY RESOLUTION
# ============================================
def resolve_deps(task_id, config, log, resolved=None):
    """Get ordered list of tasks to run (including stale dependencies)"""
    if resolved is None:
        resolved = []

    task = config.get("tasks", {}).get(task_id, {})
    deps = task.get("depends_on", [])

    for dep in deps:
        if dep not in resolved and not is_fresh(dep, config, log):
            resolve_deps(dep, config, log, resolved)
            if dep not in resolved:
                resolved.append(dep)

    if task_id not in resolved:
        resolved.append(task_id)

    return resolved


# ============================================
# RUN SINGLE TASK
# ============================================
def run_task(task_id, config, log, force=False, quiet=False):
    """Run a single task. Returns True if success."""
    task = config.get("tasks", {}).get(task_id)
    if not task:
        print(f"  [?] Unknown task: {task_id}")
        return False

    if not task.get("enabled", True):
        if not quiet:
            print(f"  [{task['name']}] DISABLED -- skipping")
        return True

    # Duplicate guard
    if task_id in _running:
        if not quiet:
            print(f"  [{task['name']}] Already running -- skipping")
        return True

    # Freshness check
    if not force and is_fresh(task_id, config, log):
        if not quiet:
            last = log["runs"][task_id]["last_success"][:16]
            print(f"  [{task['name']}] FRESH (last: {last}) -- skipping")
        return True

    # Build script path
    script_dir = task.get("script_dir")
    if script_dir:
        script = os.path.join(PROJECT_DIR, script_dir, task["script"])
    else:
        script = os.path.join(LEGACY_PYTHON_DIR, task["script"])

    if not os.path.exists(script):
        print(f"  [{task['name']}] Script not found: {script}")
        return False

    args = task.get("args", [])
    cmd = [PYTHON, script] + [str(a) for a in args]
    ts = datetime.now().strftime("%H:%M:%S")

    print(f"\n  {'='*55}")
    print(f"  [{ts}] {task['name']} -- {task['script']} {' '.join(str(a) for a in args)}")
    print(f"  {'='*55}")

    _running.add(task_id)
    start = datetime.now()

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # Longer timeout for import (reports take 15+ min)
        timeout = task.get("timeout_sec", 1800)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)

        duration = (datetime.now() - start).total_seconds()
        success = result.returncode == 0

        # Print output (last 10 lines)
        if result.stdout:
            for line in result.stdout.strip().split('\n')[-10:]:
                print(f"    {line}")

        if result.stderr and not success:
            for line in result.stderr.strip().split('\n')[-5:]:
                print(f"    ERROR: {line}")

        # Log result
        prev = log.get("runs", {}).get(task_id, {})
        log.setdefault("runs", {})[task_id] = {
            "last_run": datetime.now().isoformat(),
            "last_success": datetime.now().isoformat() if success else prev.get("last_success"),
            "success": success,
            "duration_sec": round(duration),
            "return_code": result.returncode
        }
        save_log(log)

        status = "OK" if success else "FAILED"
        print(f"  [{task['name']}] {status} ({duration:.0f}s)")
        return success

    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start).total_seconds()
        print(f"  [{task['name']}] TIMEOUT ({duration:.0f}s)")
        log.setdefault("runs", {})[task_id] = {
            "last_run": datetime.now().isoformat(),
            "success": False,
            "error": "timeout"
        }
        save_log(log)
        return False

    except Exception as e:
        print(f"  [{task['name']}] ERROR: {str(e)}")
        return False

    finally:
        _running.discard(task_id)


# ============================================
# RUN PIPELINE
# ============================================
def run_pipeline(pipeline_name, config, log, force=False):
    """Run a named pipeline (ordered list of tasks)"""
    pipeline = config.get("pipelines", {}).get(pipeline_name, [])
    if not pipeline:
        print(f"  Unknown pipeline: {pipeline_name}")
        return {}

    ts = datetime.now().strftime("%d %B %Y, %I:%M %p")
    print(f"\n{'='*60}")
    print(f"  PIPELINE: {pipeline_name.upper()} ({len(pipeline)} tasks)")
    print(f"  {ts}")
    print(f"{'='*60}")

    results = {}
    for task_id in pipeline:
        success = run_task(task_id, config, log, force=force)
        results[task_id] = success
        if not success:
            name = config.get("tasks", {}).get(task_id, {}).get("name", task_id)
            print(f"\n  WARNING: {name} failed. Continuing pipeline...")

    ok = sum(1 for v in results.values() if v)
    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE: {ok}/{len(results)} tasks succeeded")
    print(f"{'='*60}")
    return results


# ============================================
# RUN FROM STEP (with auto-dependencies)
# ============================================
def run_from(task_id, config, log):
    """Run a task + auto-resolve stale dependencies"""
    print(f"\n  Resolving dependencies for: {task_id}")
    tasks = resolve_deps(task_id, config, log)
    print(f"  Execution plan: {' -> '.join(tasks)}")

    for t in tasks:
        fresh = is_fresh(t, config, log)
        name = config.get("tasks", {}).get(t, {}).get("name", t)
        status = "FRESH (skip)" if fresh and t != task_id else "WILL RUN"
        print(f"    {name}: {status}")

    print()
    for t in tasks:
        if t == task_id or not is_fresh(t, config, log):
            run_task(t, config, log)


# ============================================
# CATCH-UP: Run all stale tasks ONCE
# ============================================
def run_catchup(config, log):
    """Check all tasks, run stale ones ONCE (in dependency order).
    This is the magic for laptop-wake-up: 6 hours missed = 1 run each, not 12."""

    all_tasks = config.get("tasks", {})
    stale = []

    for tid, task in all_tasks.items():
        if not task.get("enabled", True):
            continue
        if not is_fresh(tid, config, log):
            if passes_daily_gate(tid, config):
                stale.append(tid)

    if not stale:
        print("  [CATCH-UP] All tasks fresh -- nothing to do")
        return

    # Build execution order respecting dependencies
    ordered = []
    for tid in stale:
        deps = resolve_deps(tid, config, log)
        for d in deps:
            if d not in ordered:
                ordered.append(d)

    # Show plan
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*60}")
    print(f"  [{ts}] CATCH-UP: {len(ordered)} stale tasks detected")
    print(f"{'='*60}")

    for tid in ordered:
        task = all_tasks.get(tid, {})
        age = get_age_hours(tid, log)
        age_str = f"{age:.1f}h ago" if age is not None else "NEVER RUN"
        fresh_h = task.get("freshness_hours", "?")
        print(f"    {task.get('name', tid):<30} last: {age_str:<14} need: every {fresh_h}h")

    print()

    # Run each ONCE
    ok = 0
    fail = 0
    for tid in ordered:
        success = run_task(tid, config, log)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\n  [CATCH-UP] Done: {ok} OK, {fail} failed")
    return ok, fail


# ============================================
# STATUS
# ============================================
def show_status(config, log):
    ts = datetime.now().strftime("%d %B %Y, %I:%M %p")
    print(f"\n{'='*75}")
    print(f"  SCHEDULER STATUS -- {ts}")
    print(f"{'='*75}")

    print(f"\n  {'Task':<30} {'Last Run':<18} {'Status':<7} {'Fresh?':<7} {'Age':<9} {'Every'}")
    print(f"  {'-'*75}")

    for task_id, task in config.get("tasks", {}).items():
        run_info = log.get("runs", {}).get(task_id, {})
        last = run_info.get("last_success", "Never")[:16] if run_info.get("last_success") else "Never"
        success = "OK" if run_info.get("success") else "FAIL" if run_info.get("last_run") else "--"
        fresh = "Yes" if is_fresh(task_id, config, log) else "No"
        enabled = "" if task.get("enabled", True) else " [OFF]"

        age = get_age_hours(task_id, log)
        age_str = f"{age:.1f}h" if age is not None else "--"
        every = f"{task.get('freshness_hours', '?')}h"

        print(f"  {task.get('name', task_id):<30} {last:<18} {success:<7} {fresh:<7} {age_str:<9} {every}{enabled}")

    # Pipelines
    print(f"\n  Pipelines:")
    for name, tasks in config.get("pipelines", {}).items():
        names = [config.get("tasks", {}).get(t, {}).get("name", t) for t in tasks]
        print(f"    {name}: {' -> '.join(names)}")

    # Stale count
    stale = [tid for tid, t in config.get("tasks", {}).items()
             if t.get("enabled", True) and not is_fresh(tid, config, log)]
    if stale:
        print(f"\n  {len(stale)} stale task(s) need catch-up: {', '.join(stale)}")


# ============================================
# DAEMON MODE
# ============================================
def run_daemon(config, log):
    """Smart daemon: freshness-based, catch-up on start, no duplicates."""

    pipeline_time = config.get("daily_pipeline_time", "08:30")
    ts = datetime.now().strftime("%H:%M:%S")

    print(f"\n{'='*60}")
    print(f"  SMART SCHEDULER v1.1 -- DAEMON MODE")
    print(f"  Started: {ts}")
    print(f"  Daily pipeline after: {pipeline_time}")
    print(f"  Tasks: {len(config.get('tasks', {}))}")
    print(f"  Press Ctrl+C to stop")
    print(f"{'='*60}")

    # ── STARTUP CATCH-UP ──
    # Laptop was off? Check all tasks, run stale ones ONCE
    print(f"\n  [STARTUP] Checking for missed tasks...")
    run_catchup(config, log)

    # ── MAIN LOOP ──
    check_interval = 60  # seconds
    last_config_reload = datetime.now()
    config_reload_interval = 300  # reload config every 5 min (pick up setting changes)

    while True:
        now = datetime.now()

        # Reload config periodically (user may change settings via dashboard)
        if (now - last_config_reload).total_seconds() > config_reload_interval:
            config = load_config()
            last_config_reload = now

        # Reload log (other processes may have updated it)
        log = load_log()

        # Check each task
        for tid, task in config.get("tasks", {}).items():
            if not task.get("enabled", True):
                continue
            if tid in _running:
                continue
            if is_fresh(tid, config, log):
                continue
            if not passes_daily_gate(tid, config):
                continue

            # Task is stale + allowed to run -> run it (with deps)
            deps = resolve_deps(tid, config, log)
            for dep_id in deps:
                if dep_id in _running:
                    continue
                if not is_fresh(dep_id, config, log):
                    run_task(dep_id, config, log)
                    # Reload log after each run
                    log = load_log()

        time.sleep(check_interval)


# ============================================
# MAIN
# ============================================
def main():
    parser = argparse.ArgumentParser(description='Grow24 AI Smart Scheduler v1.1')
    parser.add_argument('--run', nargs='+', help='Run: daily, monitor, weekly, task <id>, from <id>')
    parser.add_argument('--status', action='store_true', help='Show task status & freshness')
    parser.add_argument('--daemon', action='store_true', help='Run continuously (main mode)')
    parser.add_argument('--catchup', action='store_true', help='Run all stale tasks once, then exit')
    parser.add_argument('--force', action='store_true', help='Force run even if fresh')
    args = parser.parse_args()

    config = load_config()
    log = load_log()

    if args.status:
        show_status(config, log)
        return 0

    if args.catchup:
        run_catchup(config, log)
        return 0

    if args.daemon:
        try:
            run_daemon(config, log)
        except KeyboardInterrupt:
            print("\n  Daemon stopped.")
        return 0

    if args.run:
        cmd = args.run[0]

        if cmd in ('daily', 'monitor', 'weekly'):
            run_pipeline(cmd, config, log, force=args.force)

        elif cmd == 'task' and len(args.run) > 1:
            task_id = args.run[1]
            run_task(task_id, config, log, force=args.force)

        elif cmd == 'from' and len(args.run) > 1:
            task_id = args.run[1]
            run_from(task_id, config, log)

        else:
            if cmd in config.get("tasks", {}):
                run_task(cmd, config, log, force=args.force)
            else:
                print(f"Unknown: {cmd}")
                print("Usage: --run daily | monitor | weekly | task <id> | from <id>")
                return 1
    else:
        parser.print_help()
        print("\nTasks:")
        for tid, t in config.get("tasks", {}).items():
            fresh = "FRESH" if is_fresh(tid, config, log) else "STALE"
            enabled = "" if t.get("enabled", True) else " [OFF]"
            print(f"  {tid:<20} {t.get('name', ''):<30} {fresh}{enabled}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
