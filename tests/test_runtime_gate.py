from __future__ import annotations

from pathlib import Path
import os
import tempfile
import unittest
from unittest import mock

from scripts import run_blender_runtime_gate as gate


class RuntimeGateTests(unittest.TestCase):
    def test_normalize_blender_exe_path_accepts_yen_separators(self) -> None:
        path = gate.normalize_blender_exe_path(
            "C:\u00a5Program Files\u00a5Blender Foundation\u00a5Blender 5.1\u00a5blender.exe"
        )

        self.assertEqual(
            str(path),
            r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe",
        )

    def test_normalize_blender_exe_path_accepts_fullwidth_yen_separators(self) -> None:
        path = gate.normalize_blender_exe_path(
            "C:\uffe5Program Files\uffe5Blender Foundation\uffe5Blender 5.1\uffe5blender.exe"
        )

        self.assertEqual(
            str(path),
            r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe",
        )

    def test_find_blender_uses_normalized_env_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            blender = Path(temp_root) / "Blender 5.1" / "blender.exe"
            blender.parent.mkdir()
            blender.write_bytes(b"stub")
            env_path = str(blender).replace("\\", "\u00a5")

            with mock.patch.dict(os.environ, {"BLENDER_EXE": env_path, "PATH": ""}):
                with mock.patch.object(gate, "STANDARD_CANDIDATES", []):
                    self.assertEqual(gate.find_blender(), blender)

    def test_find_blender_accepts_env_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            blender = Path(temp_root) / "Blender" / "blender.exe"
            blender.parent.mkdir()
            blender.write_bytes(b"stub")

            with mock.patch.dict(os.environ, {"BLENDER_EXE": str(blender.parent), "PATH": ""}):
                with mock.patch.object(gate, "STANDARD_CANDIDATES", []):
                    self.assertEqual(gate.find_blender(), blender)

    def test_standard_candidates_include_reported_steam_path(self) -> None:
        self.assertIn(
            Path(r"D:\SteamLibrary\steamapps\common\Blender\blender.exe"),
            gate.STANDARD_CANDIDATES,
        )

    def test_not_run_payload_includes_env_path_evidence(self) -> None:
        env_path = r"C:\missing\Blender 5.1\blender.exe"
        with mock.patch.dict(os.environ, {"BLENDER_EXE": env_path, "PATH": ""}):
            with mock.patch.object(gate, "STANDARD_CANDIDATES", []):
                payload = gate.build_not_run_payload()

        self.assertEqual(payload["status"], "not_run")
        self.assertEqual(payload["env_path"], env_path)
        self.assertFalse(payload["env_path_exists"])
        self.assertFalse(payload["env_path_normalized_exists"])
        self.assertEqual(payload["checked_paths"], [env_path])
        self.assertIn("BLENDER_EXE does not point", payload["reason"])


if __name__ == "__main__":
    unittest.main()
