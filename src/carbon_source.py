from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


@dataclass
class CarbonPoint:
    timestamp: datetime
    region: str
    carbon_intensity: float


class CarbonSource:
    """
    Loads carbon intensity data from a CSV and provides simple queries.
    """

    def __init__(self, csv_path: str):
        path = Path(csv_path)
        self.df = pd.read_csv(path, parse_dates=["timestamp"])

    def get_series(self, region: str) -> pd.DataFrame:
        return self.df[self.df["region"] == region].sort_values("timestamp")

    def avg_intensity_in_window(
        self, region: str, start: datetime, duration_hours: float
    ) -> float:
        """Average carbon intensity for [start, start+duration]."""
        end = start + timedelta(hours=duration_hours)
        series = self.get_series(region)
        mask = (series["timestamp"] >= start) & (series["timestamp"] <= end)
        window = series[mask]

        if window.empty:
            # fallback: nearest point
            if series.empty:
                raise ValueError(f"No carbon data for region {region}")
            nearest_idx = (series["timestamp"] - start).abs().idxmin()
            return float(series.loc[nearest_idx, "carbon_intensity"])

        return float(window["carbon_intensity"].mean())
