#!/usr/bin/env python3
"""
GoAmrita - Windows Scheduler Sync Engine v1.0
==============================================
Reads config_features.json and auto-syncs to Windows Task Scheduler.

Rules:
  - Feature enabled  + schedule != none  → Create/Update Windows Task
  - Feature disabled OR schedule = none  → Delete Windows Task (if exists)
  - Schedule change → Delete old + Create new (auto-handled)

Task naming: GoAmrita_<feature_id>  (e.g. GoAmrita_import, GoAmrita_buybox)

Usage:
    python scheduler_sync_v1.0.py              (sync all features)
    python scheduler_sync_v1.0.py --list       (show current Windows tasks)
    python scheduler_sync_v1.0.py --dry-run    (preview changes, no execute)
    python scheduler_sync_v1.0.py --feature import  (sync single feature)
"""

import json
import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# Windows console UTF-8 fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


def find_project_dir(start_dir: Path) -> Path:
    current = start_dir.resolve()
    while True:
        if (current / "config_features.json").exists():
            return current
        if current.parent == current:
            raise RuntimeError("Project root not found for scheduler sync")
        current = current.parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
FEATURES_CONFIG = PROJECT_DIR / "config_features.json"
PYTHON = sys.executable
TASK_PREFIX = "GoAmrita_"
LEGACY_PYTHON_DIR = PROJECT_DIR / "ClaudeCode" / "Python"
LOG_FILE = PROJECT_DIR / "ClaudeCode" / "scheduler_sync_log.json"

# ─────────────────────────────────────────
# Schedule type → schtasks arguments
# ─────────────────────────────────────────
def build_schedule_args(schedule: str, schedule_time: str = "08:30") -> str | None:
    """
    Returns schtasks /sc ... string or None if no task needed.
    """
    s = schedule.lower().strip()
    t = schedule_time or "08:30"

    if s == "none" or not s:
        return None
    if s == "daily":
        return f"/sc DAILY /st {t}"
    if s == "every_30min":
        return f"/sc MINUTE /mo 30 /st {t}"
    if s == "every_2hr":
        return f"/sc HOURLY /mo 2 /st {t}"
    if s == "every_4hr":
        return f"/sc HOURLY /mo 4 /st {t}"
    if s == "every_8hr":
        return f"/sc HOURLY /mo 8 /st {t}"
    if s == "every_12hr":
        return f"/sc HOURLY /mo 12 /st {t}"
    if s == "every_15days":
        return f"/sc DAILY /mo 15 /st {t}"
    if s == "weekly":
        return f"/sc WEEKLY /d SUN /st {t}"

    # Unknown schedule → skip
    print(f"  [WARN] Unknown schedule type: {schedule!r} — skipping")
    return None


# ─────────────────────────────────────────
# Windows Task Scheduler helpers
# ─────────────────────────────────────────
def run_ps(script: str) -> subprocess.CompletedProcess:
    """Run PowerShell command — handles spaces in paths correctly."""
    return subprocess.run(
        ['powershell', '-NonInteractive', '-NoProfile', '-Command', script],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )


def task_exists(task_name: str) -> bool:
    result = run_ps(f'Get-ScheduledTask -TaskName "{task_name}" -ErrorAction SilentlyContinue')
    return bool(result.stdout.strip())


def delete_task(task_name: str, dry_run: bool = False) -> bool:
    if not task_exists(task_name):
        return True
    if dry_run:
        print(f"  [DRY-RUN] Would delete: {task_name}")
        return True
    result = run_ps(f'Unregister-ScheduledTask -TaskName "{task_name}" -Confirm:$false')
    return result.returncode == 0


def build_ps_schedule(schedule_args: str, schedule: str, schedule_time: str) -> str:
    """Build PowerShell New-ScheduledTaskTrigger command from schedule string."""
    s = schedule.lower().strip()
    t = schedule_time or "08:30"
    h, m = (t.split(":") + ["00"])[:2]

    if s == "daily":
        return f'New-ScheduledTaskTrigger -Daily -At "{t}"'
    if s == "every_30min":
        return f'New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 30) -Once -At "{t}"'
    if s == "every_2hr":
        return f'New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 2) -Once -At "{t}"'
    if s == "every_4hr":
        return f'New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 4) -Once -At "{t}"'
    if s == "every_8hr":
        return f'New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 8) -Once -At "{t}"'
    if s == "every_12hr":
        return f'New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 12) -Once -At "{t}"'
    if s == "every_15days":
        return f'New-ScheduledTaskTrigger -Daily -DaysInterval 15 -At "{t}"'
    if s == "weekly":
        return f'New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "{t}"'
    return None


def create_task(task_name: str, python_exe: str, script_path: str,
                script_args: str, schedule: str, schedule_time: str,
                description: str, dry_run: bool = False) -> bool:
    """Create Windows Scheduled Task using PowerShell Register-ScheduledTask."""

    trigger_cmd = build_ps_schedule(None, schedule, schedule_time)
    if not trigger_cmd:
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would create: {task_name}")
        print(f"            Schedule : {schedule} at {schedule_time}")
        print(f"            Script   : {script_path}")
        return True

    # Delete existing first (clean update)
    delete_task(task_name, dry_run=False)

    # Build PowerShell script
    args_escaped = script_args.replace("'", "''") if script_args else ""
    script_path_escaped = str(script_path).replace("'", "''")
    python_escaped = str(python_exe).replace("'", "''")

    # All arguments as one quoted string for -Argument parameter
    if args_escaped:
        full_args = f'"{script_path_escaped} {args_escaped}"'
    else:
        full_args = f'"{script_path_escaped}"'

    work_dir = str(script_path).rsplit('\\', 1)[0].replace("'", "''")

    ps_script = f"""
$action  = New-ScheduledTaskAction -Execute '{python_escaped}' -Argument {full_args} -WorkingDirectory '{work_dir}'
$trigger = {trigger_cmd}
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName '{task_name}' -Action $action -Trigger $trigger -Settings $settings -Description '{description}' -Force
"""
    result = run_ps(ps_script)
    if result.returncode != 0 and result.stderr.strip():
        print(f"    [DEBUG] {result.stderr.strip()[:150]}")
    return result.returncode == 0


def list_goamrita_tasks() -> list:
    result = run_ps(
        f'Get-ScheduledTask | Where-Object {{$_.TaskName -like "{TASK_PREFIX}*"}} | '
        f'Select-Object TaskName, State | ConvertTo-Json'
    )
    tasks = []
    try:
        data = json.loads(result.stdout)
        if isinstance(data, dict):
            data = [data]
        for t in data:
            tasks.append({'name': t.get('TaskName', ''), 'status': str(t.get('State', ''))})
    except Exception:
        pass
    return tasks


# ─────────────────────────────────────────
# Main Sync Logic
# ─────────────────────────────────────────
def sync(feature_filter: str = None, dry_run: bool = False) -> dict:
    """
    Sync config_features.json → Windows Task Scheduler.
    Returns result summary dict.
    """
    if not FEATURES_CONFIG.exists():
        print(f"[ERROR] config_features.json not found at {FEATURES_CONFIG}")
        return {"error": "config_features.json not found"}

    with open(FEATURES_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    features = config.get("features", {})
    results = {"created": [], "deleted": [], "skipped": [], "failed": [], "timestamp": datetime.now().isoformat()}

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}GoAmrita Scheduler Sync — {len(features)} features")
    print("=" * 55)

    for fid, feat in features.items():
        # Filter to single feature if requested
        if feature_filter and fid != feature_filter:
            continue

        task_name = f"{TASK_PREFIX}{fid}"
        enabled   = feat.get("enabled", True)
        schedule  = feat.get("schedule", "none")
        sched_time = feat.get("schedule_time", "08:30")
        script    = feat.get("script", "")
        args      = " ".join(str(a) for a in feat.get("args", []))
        name      = feat.get("name", fid)

        schedule_args = build_schedule_args(schedule, sched_time)

        # ── CASE 1: Disabled OR no schedule → Delete task
        if not enabled or not schedule_args:
            reason = "disabled" if not enabled else "no schedule"
            if task_exists(task_name):
                ok = delete_task(task_name, dry_run=dry_run)
                status = "deleted" if ok else "failed"
                symbol = "🗑️" if ok else "❌"
                print(f"  {symbol} {name:<30} [{reason}] → task removed")
                (results["deleted"] if ok else results["failed"]).append(fid)
            else:
                print(f"  ⏭️  {name:<30} [{reason}] → no task (ok)")
                results["skipped"].append(fid)
            continue

        # ── CASE 2: Enabled + has schedule → Create/Update task
        # Support optional script_dir for modules outside ClaudeCode/Python/
        custom_dir = feat.get("script_dir", "")
        if custom_dir:
            script_path = PROJECT_DIR / custom_dir / script
        else:
            script_path = LEGACY_PYTHON_DIR / script
        ok = create_task(
            task_name=task_name,
            python_exe=PYTHON,
            script_path=script_path,
            script_args=args,
            schedule=schedule,
            schedule_time=sched_time,
            description=name,
            dry_run=dry_run
        )
        if ok:
            print(f"  ✅ {name:<30} [{schedule}] → task {'updated' if task_exists(task_name) else 'created'}")
            results["created"].append(fid)
        else:
            print(f"  ❌ {name:<30} → FAILED to create task")
            results["failed"].append(fid)

    # ── Save log
    if not dry_run:
        try:
            log = []
            if LOG_FILE.exists():
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    log = json.load(f)
                if not isinstance(log, list):
                    log = []
            log.insert(0, results)
            log = log[:20]  # keep last 20 syncs
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  [WARN] Could not save log: {e}")

    print("=" * 55)
    print(f"  Created/Updated : {len(results['created'])}")
    print(f"  Deleted         : {len(results['deleted'])}")
    print(f"  Skipped         : {len(results['skipped'])}")
    print(f"  Failed          : {len(results['failed'])}")
    if results["failed"]:
        print(f"  Failed list     : {results['failed']}")

    return results


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GoAmrita Windows Scheduler Sync")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    parser.add_argument("--list",    action="store_true", help="List current GoAmrita tasks")
    parser.add_argument("--feature", type=str, default=None, help="Sync single feature only")
    args = parser.parse_args()

    if args.list:
        tasks = list_goamrita_tasks()
        if not tasks:
            print("No GoAmrita tasks found in Windows Scheduler.")
        else:
            print(f"\n{'Task Name':<35} {'Next Run':<25} {'Status'}")
            print("-" * 75)
            for t in tasks:
                print(f"  {t['name']:<33} {t.get('next_run',''):<25} {t.get('status','')}")
        sys.exit(0)

    sync(feature_filter=args.feature, dry_run=args.dry_run)
