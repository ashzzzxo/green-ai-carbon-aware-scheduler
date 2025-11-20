# Green AI – Carbon-Aware Training Scheduler: User Guide

This guide explains how to configure, run, and interpret the
**Green AI – Carbon-Aware Training Scheduler**.

The goal of the tool is to:
- Read carbon intensity data for multiple regions.
- Choose a low-carbon region and start time for a training job, subject to a deadline.
- Estimate carbon savings compared to a baseline “run now in default region” policy.
- Launch the training script and log the results.

---

## 1. Prerequisites

- Python 3.9+ installed.
- Git / command line access.
- Recommended: a virtual environment for Python packages.

---

## 2. Installation

From the project root:

```bash
pip install -r requirements.txt
