from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "docs" / "qcds-strict-metrics.json"
ALLOWED = {"S+", "S-", "A+", "A-", "B+", "B-", "C+", "C-", "D+", "D-"}
REQUIRED = {"Quality", "Cost", "Delivery", "Satisfaction"}


def main() -> None:
    data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    ratings = data.get("ratings", {})
    missing = REQUIRED - set(ratings)
    if missing:
        raise SystemExit(f"missing QCDS ratings: {sorted(missing)}")
    bad = {key: value for key, value in ratings.items() if value not in ALLOWED}
    if bad:
        raise SystemExit(f"invalid QCDS ratings: {bad}")

    runtime_status = data.get("runtime_gate", {}).get("status")
    if runtime_status != "passed":
        for key in ("Quality", "Satisfaction"):
            if ratings.get(key) not in {"B+", "B-", "C+", "C-", "D+", "D-"}:
                raise SystemExit(
                    f"{key} must be B+ or lower when runtime gate is not passed"
                )
    print("QCDS metrics are valid")


if __name__ == "__main__":
    main()

