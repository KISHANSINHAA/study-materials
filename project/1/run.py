"""
Convenience launcher for local development.

Usage:
    python run.py api          # FastAPI on :8000
    python run.py ui           # Streamlit on :8501
    python run.py both         # both, in subprocesses
"""

from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run_api():
    return subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "api.main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload",
        ],
        cwd=ROOT,
    )


def _run_ui():
    return subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            str(ROOT / "app" / "streamlit_app.py"),
            "--server.port", "8501",
        ],
        cwd=ROOT,
    )


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ui"
    procs = []

    if cmd == "api":
        procs.append(_run_api())
    elif cmd == "ui":
        procs.append(_run_ui())
    elif cmd == "both":
        procs.append(_run_api())
        time.sleep(1.5)
        procs.append(_run_ui())
    else:
        print(__doc__)
        return 1

    def _stop(_sig, _frame):
        for p in procs:
            try:
                p.terminate()
            except Exception:  # noqa: BLE001
                pass
        sys.exit(0)

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        _stop(None, None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
