# Green AI – Carbon-Aware Training Scheduler: User Guide

This guide shows you how to configure, run, and interpret the **Green AI – Carbon-Aware Training Scheduler**.

The tool helps you:

- Read carbon intensity data for multiple regions.
- Choose a low-carbon region and start time for a training job, subject to a deadline.
- Estimate carbon savings compared to a baseline “run now in default region” policy.
- Launch a training script and log results.

---

## 1. Prerequisites

- Python 3.9+ installed.
- Git / command line access.
- Recommended: a Python virtual environment (e.g., `venv` or `conda`).

Optional but useful:

- Jupyter Notebook (to explore `results.csv` and plots).
- Basic familiarity with YAML configuration files.

---

## 2. Installation

From the project root:

```bash
pip install -r requirements.txt
This installs core dependencies such as pandas and python-dateutil.

If you are using a virtual environment:

bash

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
---
## 3. Project Layout 
At a high level, you will mainly work with:

jobs/ – YAML job configuration files (you will create/edit these).

carbon_data/carbon_data.csv – carbon intensity data (you may replace this with your own data).

src/runner.py – command-line entry point to run the scheduler.

results.csv – log of scheduling decisions and metrics, created after runs.

Supporting components such as JobConfig, CarbonSource, and Scheduler live in src/ and are documented in DESIGN.md if you want to extend the system.
---

## 4. Defining a Training Job (YAML)
Each training job is defined by a YAML file under jobs/. A typical example:

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
Field summary:

**job_name**
Unique name for the job. Used in logs and plots.

**script**
Path to the training script to execute (e.g., train_model.py). In this prototype, the script is a dummy workload, but you can replace it with your own training entry point.

**deadline**
Latest acceptable completion time, in ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS). The scheduler only considers start times that allow the job to finish before this deadline.

**job_class**
Placeholder for future policies (e.g., “deadline-flexible”, “cost-sensitive”). In the current prototype, this is informational only.

**preferred_regions**
List of regions the scheduler is allowed to consider (e.g., us-east, us-west, eu-north). These must match region names in carbon_data.csv.

**max_cost_per_hour**
Reserved for future cost-aware scheduling. Currently not used in decisions, but kept in the configuration for extensibility.

**est_duration_hours**
Estimated training duration, in hours. Used to compute how far back from the deadline we can start the job.

**default_region**
Region used for the baseline “run now in default region” policy. Must match a region in the carbon data.

To create your own job, copy an existing YAML file (e.g., jobs/example_job.yaml), modify the fields, and save under a new name.
---

## 5. Carbon-Intensity Data
Carbon-intensity data lives in:


carbon_data/carbon_data.csv
The format is:
timestamp,region,carbon_intensity
2025-11-20T10:00:00,us-east,450
2025-11-20T10:00:00,us-west,300
2025-11-20T10:00:00,eu-north,150
...
Columns:

**timestamp** – ISO 8601 time of the measurement.

**region** – region identifier (e.g., us-east).

**carbon_intensity** – relative carbon score at that time and region.

**Note: The scheduler assumes that all preferred_regions and default_region values in your job YAML exist in this CSV.**

You can replace this file with your own data as long as you keep the same column names and timestamp format.
---

## 6. Running the Scheduler
From the project root, run:


python -m src.runner --job-path jobs/example_job.yaml
Key options:

--job-path
Path to the YAML file defining the job.

Internally, the runner will:

Load the job configuration.

Load carbon data via CarbonSource.

Call the scheduler to pick:

a start time, and

a region with minimum average carbon intensity before the deadline.

Compute baseline vs carbon-aware emission scores.

Log metrics to results.csv.

Launch the training script (e.g., train_model.py) using subprocess.

If the job’s deadline has already passed (or the latest feasible start time is in the past), the scheduler treats the job as urgent and starts it immediately in the best available region.
---

## 7. Understanding the Output
**7.1 Console Output**
On a successful run, you’ll see console messages summarizing:

The chosen region and start time.

The baseline emission score (run now in default_region).

The carbon-aware emission score.

The estimated savings percentage.

Example (simplified):

[Scheduler] Job: resnet_cifar10
[Scheduler] Chosen region: eu-north
[Scheduler] Chosen start: 2025-11-20T15:00:00
[Metrics] Baseline score: 900
[Metrics] Carbon-aware score: 300
[Metrics] Savings: 66.7%
**7.2 results.csv**
Each run appends a row to results.csv in the project root. Typical columns:

job_name

chosen_region

chosen_start

baseline_emission_score

actual_emission_score

savings_pct

You can open this file in Excel, or load it into a notebook:

import pandas as pd

df = pd.read_csv("results.csv")
print(df.tail())
---
## 8. Visualizing Carbon Savings (Optional)
The repository includes a Jupyter notebook:

notebooks/analysis.ipynb
This notebook:

Loads results.csv.

Plots savings percentage per job.

Optionally shows baseline vs carbon-aware emission scores side by side.

To use it:

Activate your virtual environment (if any).

Start Jupyter:

jupyter notebook
Open notebooks/analysis.ipynb and run the cells.
---

## 9. Customizing and Extending
Here are a few simple ways to explore the tool:

Change job deadlines and durations
See how a tighter or looser deadline affects the scheduler’s ability to find low-carbon windows.

Modify carbon data
Edit or replace carbon_data.csv with another set of regions or a different carbon pattern.

Swap the training script
Point the script field in your job YAML to your own training entry point (e.g., a real model training script). Make sure it can be called from the command line.

For deeper architectural details (JobConfig, CarbonSource, Scheduler internals), refer to DESIGN.md.
---

## 10. Troubleshooting
The scheduler says no data found for a region/time window

Check that all region names in your YAML exist in carbon_data.csv.

Check that timestamps in carbon_data.csv cover the window between now and deadline.

Deadline-related issues

If your deadline is earlier than the current time, the job will be treated as urgent. Update the deadline field to a future time.

Import or module errors

Make sure you are running commands from the project root.

Verify that pip install -r requirements.txt completed without errors.

If you plan to integrate this prototype with cloud schedulers or MATLAB-based workflows, see the “Extensibility and Integration” section in the design document.

If you want the file version I just wrote in the environment, you can treat it as:

`/mnt/data/USER_GUIDE_POLISHED.md`





