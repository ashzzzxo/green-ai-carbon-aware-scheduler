import argparse
import subprocess
from datetime import datetime

from .job import load_job_config
from .carbon_source import CarbonSource
from .scheduler import Scheduler
from .metrics import append_decision


def run_job_with_schedule(job_config_path: str, carbon_csv: str):
    job = load_job_config(job_config_path)
    carbon_source = CarbonSource(carbon_csv)
    scheduler = Scheduler(carbon_source)

    now = datetime.now()
    decision = scheduler.schedule_job(job, now=now)

    print(f"[SCHEDULER] Job: {decision.job_name}")
    print(f"  Region:        {decision.region}")
    print(f"  Start time:    {decision.start_time}")
    print(f"  Est. end time: {decision.est_end_time}")
    print(f"  Savings:       {decision.savings_pct:.2f}% vs baseline")

    append_decision(decision)

    # MVP: just run immediately (we're not waiting until future start time yet)
    print("[RUNNER] Launching training script now...")
    subprocess.run(["python", job.script], check=True)


def main():
    parser = argparse.ArgumentParser(description="Green AI Carbon-Aware Scheduler Runner")
    parser.add_argument("--job-config", required=True, help="Path to job YAML file")
    parser.add_argument(
        "--carbon-csv",
        default="carbon_data/carbon_data.csv",
        help="Path to carbon intensity CSV",
    )
    args = parser.parse_args()

    run_job_with_schedule(args.job_config, args.carbon_csv)


if __name__ == "__main__":
    main()
