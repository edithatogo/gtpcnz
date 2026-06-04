from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    base = root / ".tmp" / f"pytest-{os.getpid()}-{int(time.time())}"
    base.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        f"--basetemp={base / 'unit'}",
        "--ignore=models/tests/test_app.py",
        "--ignore=models/tests/test_streamlit_dashboard_app.py",
        "--ignore=models/tests/test_streamlit_end_to_end_smoke.py",
        "--ignore=models/tests/test_streamlit_post_labs.py",
        *sys.argv[1:],
    ]
    env = {**dict(os.environ), "LOKY_MAX_CPU_COUNT": "2"}
    completed = subprocess.run(command, check=False, env=env, capture_output=True, text=True)
    if completed.stdout:
        print(completed.stdout, end="")
    stderr = completed.stderr
    benign_temp_cleanup = (
        "weakref.py" in stderr
        and "tempfile.py" in stderr
        and "PermissionError: [WinError 5] Access is denied" in stderr
    )
    benign_pytest_basetemp_cleanup = (
        "cleanup_dead_symlinks" in stderr
        and "PermissionError: [WinError 5] Access is denied" in stderr
        and ".tmp" in stderr
        and "pytest-" in stderr
    )
    real_pytest_failure = any(marker in completed.stdout for marker in ("FAILED", "ERRORS", "ERROR at"))
    benign_teardown = benign_temp_cleanup or benign_pytest_basetemp_cleanup
    if stderr and ((completed.returncode != 0 and real_pytest_failure) or not benign_teardown):
        print(stderr, end="", file=sys.stderr)
    if completed.returncode != 0 and not (benign_teardown and not real_pytest_failure):
        return completed.returncode

    smoke = subprocess.run(
        [sys.executable, "scripts/run_streamlit_e2e_smoke.py"],
        check=False,
        env=env,
        capture_output=True,
        text=True,
    )
    if smoke.stdout:
        print(smoke.stdout, end="")
    smoke_stderr = smoke.stderr
    smoke_benign_temp_cleanup = (
        "weakref.py" in smoke_stderr
        and "tempfile.py" in smoke_stderr
        and "PermissionError: [WinError 5] Access is denied" in smoke_stderr
    )
    if smoke_stderr and (smoke.returncode != 0 or not smoke_benign_temp_cleanup):
        print(smoke_stderr, end="", file=sys.stderr)
    return smoke.returncode


if __name__ == "__main__":
    raise SystemExit(main())
