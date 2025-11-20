from dataclasses import dataclass
from datetime import datetime
from typing import List
from pathlib import Path
import yaml


@dataclass
class JobConfig:
    job_name: str
    script: str
    deadline: datetime
    job_class: str
    preferred_regions: List[str]
    max_cost_per_hour: float
    est_duration_hours: float
    default_region: str


def load_job_config(path: str) -> JobConfig:
    path_obj = Path(path)
    with path_obj.open() as f:
        data = yaml.safe_load(f)

    return JobConfig(
        job_name=data["job_name"],
        script=data["script"],
        deadline=datetime.fromisoformat(data["deadline"]),
        job_class=data.get("job_class", "deadline-flexible"),
        preferred_regions=data["preferred_regions"],
        max_cost_per_hour=float(data.get("max_cost_per_hour", 0.0)),
        est_duration_hours=float(data["est_duration_hours"]),
        default_region=data.get("default_region", data["preferred_regions"][0]),
    )
