from pathlib import Path
import csv
from datetime import datetime

from .scheduler import ScheduleDecision

RESULTS_HEADER = [
    "timestamp_logged",
    "job_name",
    "region",
    "start_time",
    "est_end_time",
    "avg_carbon_intensity",
    "baseline_carbon",
    "actual_carbon",
    "savings_pct",
]


def append_decision(decision: ScheduleDecision, path: str = "results.csv") -> None:
    path_obj = Path(path)
    file_exists = path_obj.exists()

    with path_obj.open("a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(RESULTS_HEADER)

        writer.writerow(
            [
                datetime.now().isoformat(),
                decision.job_name,
                decision.region,
                decision.start_time.isoformat(),
                decision.est_end_time.isoformat(),
                f"{decision.avg_carbon_intensity:.2f}",
                f"{decision.baseline_carbon:.2f}",
                f"{decision.actual_carbon:.2f}",
                f"{decision.savings_pct:.2f}",
            ]
        )
