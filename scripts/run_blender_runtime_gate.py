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
PACKAGE = DIST / "blender-auto-backup-0.1.1.zip"
EXPECTED_VERSION = "Blender 4.2+; user validation target is 5.1.1"
STANDARD_CANDIDATES = [
    Path(r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"),
    Path(r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"),
    Path(r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"),
    Path(r"C:\Program Files\Blender Foundation\Blender\blender.exe"),
    Path(r"D:\SteamLibrary\steamapps\common\Blender\blender.exe"),
    Path(r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"),
    Path(r"C:\Program Files\Steam\steamapps\common\Blender\blender.exe"),
]
MAX_REPORTED_CANDIDATES = 24


def normalize_blender_exe_path(value: str) -> Path:
    normalized = value.strip().strip('"').strip("'")
    normalized = normalized.replace("\u00a5", "\\").replace("\uffe5", "\\")
    normalized = os.path.expandvars(normalized)
    return Path(normalized).expanduser()


def blender_exe_candidate(path: Path) -> Path:
    if path.name.lower() == "blender.exe":
        return path
    return path / "blender.exe"


def candidate_paths() -> list[Path]:
    env_path = os.environ.get("BLENDER_EXE")
    candidates: list[Path] = []
    if env_path:
        candidates.append(blender_exe_candidate(normalize_blender_exe_path(env_path)))
    candidates.extend(STANDARD_CANDIDATES)
    path_env = os.environ.get("PATH", "")
    for entry in path_env.split(os.pathsep):
        if entry:
            candidates.append(Path(entry) / "blender.exe")
    return _dedupe_paths(candidates)


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path).casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


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


def build_not_run_payload() -> dict:
    env_path = os.environ.get("BLENDER_EXE")
    candidates = candidate_paths()
    payload: dict = {
        "status": "not_run",
        "reason": "blender.exe was not found. Set BLENDER_EXE to run the gate.",
        "expected_version": EXPECTED_VERSION,
        "checked_path_count": len(candidates),
        "checked_paths": [str(path) for path in candidates[:MAX_REPORTED_CANDIDATES]],
    }
    if len(candidates) > MAX_REPORTED_CANDIDATES:
        payload["checked_paths_truncated"] = True

    if env_path:
        normalized = normalize_blender_exe_path(env_path)
        env_candidate = blender_exe_candidate(normalized)
        payload.update(
            {
                "reason": "BLENDER_EXE does not point to a blender.exe file and no fallback blender.exe was found.",
                "env_path": env_path,
                "env_path_exists": Path(env_path).is_file(),
                "env_path_is_dir": normalized.is_dir(),
                "env_path_normalized": str(normalized),
                "env_path_normalized_exists": normalized.is_file(),
                "env_candidate": str(env_candidate),
                "env_candidate_exists": env_candidate.is_file(),
                "hint": "Verify the path with Test-Path -LiteralPath $env:BLENDER_EXE, or set BLENDER_EXE to the actual Blender 5.1.1 blender.exe.",
            }
        )
    return payload


def main() -> None:
    blender = find_blender()
    if blender is None:
        payload = build_not_run_payload()
        write_result(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return

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
