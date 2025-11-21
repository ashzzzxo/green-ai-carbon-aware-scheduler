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
