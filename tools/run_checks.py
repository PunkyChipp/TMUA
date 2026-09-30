"""Run every content/checks/*_check.py (sympy / brute-force answer verification)."""
import pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent / "content" / "checks"
failed = []
for f in sorted(root.glob("*_check.py")):
    r = subprocess.run([sys.executable, f.name], cwd=root, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or [""])[-1] if r.returncode == 0 else (r.stderr.strip().splitlines() or ["?"])[-1]
    print(f"{f.stem:16} {'ok ' if r.returncode == 0 else 'FAIL'}  {last}")
    if r.returncode:
        failed.append(f.name)
sys.exit(1 if failed else 0)
