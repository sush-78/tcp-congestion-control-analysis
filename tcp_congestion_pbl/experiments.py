"""Repeatable predefined network experiment comparisons."""
from dataclasses import replace
import pandas as pd
from simulator import SimulationConfig, run_simulation
from metrics import calculate_metrics

EXPERIMENT_PRESETS = {
    "Low network congestion": {"congestion_level": "Low", "packet_loss_pct": 1.0},
    "Medium network congestion": {"congestion_level": "Medium", "packet_loss_pct": 2.0},
    "High network congestion": {"congestion_level": "High", "packet_loss_pct": 5.0},
    "Low packet loss": {"congestion_level": "Medium", "packet_loss_pct": 0.2},
    "High packet loss": {"congestion_level": "Medium", "packet_loss_pct": 12.0},
}
def run_preset_experiment(base_config: SimulationConfig, preset_name: str):
    if preset_name == "Tahoe vs Reno":
        configs = [replace(base_config, algorithm=a) for a in ("Tahoe", "Reno")]
    else:
        if preset_name not in EXPERIMENT_PRESETS: raise ValueError(f"Unknown preset: {preset_name}")
        configs = [replace(base_config, **EXPERIMENT_PRESETS[preset_name], algorithm=a) for a in ("Tahoe", "Reno")]
    rows = []
    for cfg in configs:
        rows.append({"experiment": preset_name, "algorithm": cfg.algorithm, **calculate_metrics(run_simulation(cfg, cfg.algorithm), cfg.duration_seconds)})
    return pd.DataFrame(rows)
