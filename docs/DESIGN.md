# Green AI – Carbon-Aware Training Scheduler: Design Overview

## 1. Goal

The Green AI – Carbon-Aware Training Scheduler is a prototype system that
explores how to reduce the carbon footprint of ML training jobs by
choosing **when** and **where** to run them.

The design aims to:

- Model training jobs with deadlines, estimated duration, and preferred regions.
- Use regional carbon intensity data to pick **low-carbon time windows**.
- Compare a **carbon-aware policy** against a baseline “run now in the
  default region” policy.
- Log metrics so engineers can analyze carbon savings and scheduling
  behavior.

Although the current implementation runs locally, the architecture is
designed to map cleanly to cloud schedulers (GCP, Kubernetes, Slurm).

---

## 2. High-Level Architecture

The system is organized into five main components:

1. **JobConfig (`src/job.py`)**  
   - Dataclass representing a training job.  
   - Loaded from a YAML file under `jobs/`.  
   - Fields: `job_name`, `script`, `deadline`, `job_class`,
     `preferred_regions`, `max_cost_per_hour`, `est_duration_hours`,
     `default_region`.

2. **CarbonSource (`src/carbon_source.py`)**  
   - Loads carbon intensity data from `carbon_data/carbon_data.csv`.  
   - Provides queries for the average intensity of a region in a given
     time window.

3. **Scheduler (`src/scheduler.py`)**  
   - Implements the core scheduling algorithm.  
   - Searches over candidate regions and start times and picks the option
     with minimum average carbon intensity while respecting the job’s
     deadline.

4. **Runner (`src/runner.py`)**  
   - Command-line entry point.  
   - Orchestrates the flow: load job, call scheduler, log metrics, and
     launch the training script via `subprocess`.

5. **Metrics Logger (`src/metrics.py`)**  
   - Appends scheduling decisions and derived metrics to `results.csv`.  
   - Metrics include baseline vs actual emission scores and
     carbon savings (%).

Supporting files:

- `train_model.py` – Dummy training script used to simulate a real ML
  workload.
- `notebooks/analysis.ipynb` – Reads `results.csv` and generates plots
  for baseline vs carbon-aware emissions.

---

## 3. Data Model

### 3.1 Job configuration

Jobs are defined by YAML files (e.g., `jobs/example_job.yaml`):

```yaml
job_name: resnet_cifar10
script: train_model.py
deadline: "2025-11-20T18:00:00"
job_class: "deadline-flexible"
preferred_regions:
  - us-east
  - us-west
  - eu-north
max_cost_per_hour: 2.0
est_duration_hours: 2.0
default_region: "us-east"
