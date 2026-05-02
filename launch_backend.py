import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = (ROOT / "runtime-live.log").open("a", encoding="utf-8")
err = (ROOT / "runtime-live.err.log").open("a", encoding="utf-8")

flags = 0
if hasattr(subprocess, "DETACHED_PROCESS"):
    flags |= subprocess.DETACHED_PROCESS
if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
    flags |= subprocess.CREATE_NEW_PROCESS_GROUP

proc = subprocess.Popen(
    [sys.executable, "app.py"],
    cwd=str(ROOT),
    stdin=subprocess.DEVNULL,
    stdout=out,
    stderr=err,
    creationflags=flags,
    close_fds=True,
)
(ROOT / "server.pid").write_text(str(proc.pid), encoding="utf-8")
print(proc.pid)
