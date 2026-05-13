from __future__ import annotations

from pathlib import Path
import compileall
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def run_python_script(relative_path: str) -> int:
    completed = subprocess.run([sys.executable, str(ROOT / relative_path)], cwd=ROOT)
    return completed.returncode


def run_unittest() -> tuple[bool, int]:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful(), result.testsRun


def main() -> None:
    DIST.mkdir(exist_ok=True)
    steps: list[dict] = []

    compile_ok = compileall.compile_dir(ROOT / "blender_auto_backup", quiet=1)
    steps.append({"name": "compile_addon", "status": "passed" if compile_ok else "failed"})
    if not compile_ok:
        write_summary(steps)
        raise SystemExit(1)

    ok, test_count = run_unittest()
    steps.append({"name": "unittest", "status": "passed" if ok else "failed", "tests": test_count})
    if not ok:
        write_summary(steps)
        raise SystemExit(1)

    for name, script in [
        ("package_addon", "scripts/package_addon.py"),
        ("collect_docs_zip", "scripts/collect_docs_zip.py"),
        ("validate_qcds", "scripts/validate_qcds.py"),
        ("check_text_integrity", "scripts/check_text_integrity.py"),
        ("runtime_gate", "scripts/run_blender_runtime_gate.py"),
    ]:
        code = run_python_script(script)
        status = "passed" if code == 0 else "failed"
        if name == "runtime_gate" and code == 0:
            runtime_path = DIST / "runtime-gate.json"
            if runtime_path.exists():
                status = json.loads(runtime_path.read_text(encoding="utf-8")).get("status", status)
        steps.append({"name": name, "status": status})
        if code != 0:
            write_summary(steps)
            raise SystemExit(code)

    write_summary(steps)


def write_summary(steps: list[dict]) -> None:
    failed = any(step["status"] == "failed" for step in steps)
    runtime_not_run = any(step["name"] == "runtime_gate" and step["status"] == "not_run" for step in steps)
    status = "failed" if failed else "passed_with_runtime_not_run" if runtime_not_run else "passed"
    payload = {"status": status, "steps": steps}
    (DIST / "test-summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
