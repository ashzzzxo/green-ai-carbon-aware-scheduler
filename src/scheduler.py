from dataclasses import dataclass
from datetime import datetime, timedelta

from .job import JobConfig
from .carbon_source import CarbonSource


@dataclass
class ScheduleDecision:
    job_name: str
    region: str
    start_time: datetime
    est_end_time: datetime
    avg_carbon_intensity: float
    baseline_carbon: float
    actual_carbon: float
    savings_pct: float


class Scheduler:
    def __init__(self, carbon_source: CarbonSource):
        self.carbon_source = carbon_source

    def _compute_baseline_carbon(self, job: JobConfig, now: datetime) -> float:
        baseline_intensity = self.carbon_source.avg_intensity_in_window(
            job.default_region, now, job.est_duration_hours
        )
        return baseline_intensity * job.est_duration_hours

    def schedule_job(
        self, job: JobConfig, now: datetime, step_hours: float = 1.0
    ) -> ScheduleDecision:
        latest_start = job.deadline - timedelta(hours=job.est_duration_hours)
        if latest_start <= now:
            latest_start = now  # must start asap

        best_region = job.default_region
        best_start = now
        best_intensity = float("inf")

        # try each region and candidate start time
        for region in job.preferred_regions:
            t = now
            while t <= latest_start:
                avg_intensity = self.carbon_source.avg_intensity_in_window(
                    region, t, job.est_duration_hours
                )
                if avg_intensity < best_intensity:
                    best_intensity = avg_intensity
                    best_region = region
                    best_start = t
                t += timedelta(hours=step_hours)

        est_end_time = best_start + timedelta(hours=job.est_duration_hours)

        baseline_carbon = self._compute_baseline_carbon(job, now)
        actual_carbon = best_intensity * job.est_duration_hours
        savings_pct = (
            (baseline_carbon - actual_carbon) / baseline_carbon * 100
            if baseline_carbon > 0
            else 0.0
        )

        return ScheduleDecision(
            job_name=job.job_name,
            region=best_region,
            start_time=best_start,
            est_end_time=est_end_time,
            avg_carbon_intensity=best_intensity,
            baseline_carbon=baseline_carbon,
            actual_carbon=actual_carbon,
            savings_pct=savings_pct,
        )
