This repo contains a carbon-aware scheduler for ML training jobs.
Given a job description (deadline, duration, allowed regions) and regional carbon-intensity data, it searches for the best time and place to run the job so that emissions are lower than a “run now in default region” baseline.
The project includes a clean architecture (JobConfig, CarbonSource, Scheduler, Runner and Metrics modules), a user guide for running real jobs, and a design document for developers who want to extend or integrate the scheduler with cloud or MATLAB workflows.
# Green AI – Carbon-Aware Training Scheduler

The **Green AI – Carbon-Aware Training Scheduler** is a toy project that explores
how to schedule ML training jobs in **low-carbon time windows** instead of
running them immediately in a default region.

The current prototype runs locally and:

- Reads **carbon intensity data** for multiple regions from a CSV file.
- Reads **job configurations** (deadline, duration, preferred regions) from YAML.
- Chooses a region + start time that **minimizes average carbon intensity**
  before the job’s deadline.
- Compares against a **baseline "run now in default region"** policy.
- Launches a training script and logs **baseline vs actual emission scores**
  and **carbon savings (%)** into `results.csv`.
- Provides a small Jupyter notebook to visualize the results.

The design is intentionally modular so it can be extended later to real carbon
APIs and cloud schedulers (e.g., GCP).

---

## 1. Project Structure

```text
greenai_scheduler/
├─ carbon_data/
│  └─ carbon_data.csv        # sample carbon intensity data by region
├─ jobs/
│  └─ example_job.yaml       # example job definition
├─ notebooks/
│  └─ analysis.ipynb         # plots: baseline vs carbon-aware
├─ src/
│  ├─ __init__.py
│  ├─ job.py                 # JobConfig dataclass + YAML loader
│  ├─ carbon_source.py       # CarbonSource: loads & queries carbon data
│  ├─ scheduler.py           # Scheduler: picks region + start time
│  ├─ runner.py              # CLI entry point: tie everything together
│  ├─ metrics.py             # metrics logger → results.csv
│  └─ utils.py               # (reserved for helpers)
├─ docs/
│  ├─ DESIGN.md              # system design / technical overview
│  └─ USER_GUIDE.md          # step-by-step usage
├─ train_model.py            # dummy training script (simulated epochs)
├─ requirements.txt
└─ README.md
