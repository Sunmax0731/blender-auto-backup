from __future__ import annotations

from pathlib import Path
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GATE_SCRIPT = ROOT / "tests" / "blender_runtime_gate.py"
PACKAGE = DIST / "blender-auto-backup-0.1.0.zip"


def candidate_paths() -> list[Path]:
    env_path = os.environ.get("BLENDER_EXE")
    candidates: list[Path] = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend(
        [
            Path(r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"),
            Path(r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"),
            Path(r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"),
            Path(r"C:\Program Files\Blender Foundation\Blender\blender.exe"),
        ]
    )
    path_env = os.environ.get("PATH", "")
    for entry in path_env.split(os.pathsep):
        if entry:
            candidates.append(Path(entry) / "blender.exe")
    return candidates


def find_blender() -> Path | None:
    for candidate in candidate_paths():
        if candidate.is_file():
            return candidate
    return None


def write_result(payload: dict) -> None:
    DIST.mkdir(exist_ok=True)
    (DIST / "runtime-gate.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    blender = find_blender()
    if blender is None:
        payload = {
            "status": "not_run",
            "reason": "blender.exe was not found. Set BLENDER_EXE to run the gate.",
            "expected_version": "Blender 4.2+; user validation target is 5.1.1",
        }
        write_result(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return

    if not PACKAGE.exists():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "package_addon.py")], cwd=ROOT, check=True)

    validation = subprocess.run(
        [str(blender), "--command", "extension", "validate", str(PACKAGE)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    DIST.mkdir(exist_ok=True)
    (DIST / "extension-validate.log").write_text(validation.stdout, encoding="utf-8")
    if validation.returncode != 0:
        payload = {
            "status": "failed",
            "gate": "extension_validate",
            "blender_exe": str(blender),
            "package": str(PACKAGE),
            "returncode": validation.returncode,
            "log": str(DIST / "extension-validate.log"),
        }
        write_result(payload)
        print(json.dumps(payload, ensure_ascii=False))
        sys.exit(1)

    command = [
        str(blender),
        "--background",
        "--factory-startup",
        "--python",
        str(GATE_SCRIPT),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    DIST.mkdir(exist_ok=True)
    (DIST / "runtime-gate.log").write_text(completed.stdout, encoding="utf-8")

    match = re.search(r"BLENDER_AUTO_BACKUP_RUNTIME_GATE=(\{.*\})", completed.stdout)
    if completed.returncode == 0 and match:
        payload = json.loads(match.group(1))
        payload["blender_exe"] = str(blender)
        payload["extension_validate"] = "passed"
        write_result(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return

    payload = {
        "status": "failed",
        "blender_exe": str(blender),
        "returncode": completed.returncode,
        "log": str(DIST / "runtime-gate.log"),
    }
    write_result(payload)
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
