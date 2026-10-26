"""Educational discrete-round TCP Tahoe/Reno simulation (not a real TCP stack)."""
from dataclasses import dataclass
import math, random

@dataclass
class SimulationConfig:
    duration_seconds: int = 30
    rtt_ms: float = 100.0
    bandwidth_mbps: float = 5.0
    packet_loss_pct: float = 2.0
    initial_cwnd: float = 1.0
    initial_ssthresh: float = 16.0
    mss_bytes: int = 1460
    seed: int = 42
    congestion_level: str = "Medium"
    scenario: str = "Recorded video lecture"
    workload_mbps: float = 3.0
    algorithm: str = "Reno"

    def validate(self):
        checks = [
            (isinstance(self.duration_seconds, int) and 1 <= self.duration_seconds <= 600, "Duration must be 1–600 seconds."),
            (1 <= self.rtt_ms <= 2000, "RTT must be 1–2000 ms."),
            (0.1 <= self.bandwidth_mbps <= 10000, "Bandwidth must be 0.1–10000 Mbps."),
            (0 <= self.packet_loss_pct <= 50, "Packet loss must be 0–50%."),
            (1 <= self.initial_cwnd <= 1000, "Initial cwnd must be 1–1000 MSS."),
            (2 <= self.initial_ssthresh <= 10000, "Initial ssthresh must be 2–10000 MSS."),
            (64 <= self.mss_bytes <= 9000, "MSS must be 64–9000 bytes."),
            (self.congestion_level in {"Low", "Medium", "High"}, "Invalid congestion level."),
            (self.scenario in {"Recorded video lecture", "Live online class", "Study-material download", "Assignment / quiz submission"}, "Invalid scenario."),
            (0.01 <= self.workload_mbps <= 10000, "Workload demand must be 0.01–10000 Mbps."),
        ]
        for valid, message in checks:
            if not valid: raise ValueError(message)

def run_simulation(config: SimulationConfig, algorithm=None):
    """Return per-RTT records. ACK/loss detection is abstracted for teaching."""
    config.validate()
    algo = (algorithm or config.algorithm).title()
    if algo not in {"Tahoe", "Reno"}: raise ValueError("Algorithm must be Tahoe or Reno.")
    rng = random.Random(config.seed)
    cwnd, ssthresh, elapsed, event_id = float(config.initial_cwnd), float(config.initial_ssthresh), 0.0, 0
    p_loss = config.packet_loss_pct / 100
    capacity = config.bandwidth_mbps * {"Low": 1.0, "Medium": .8, "High": .55}[config.congestion_level]
    scenario_factor = {"Recorded video lecture": 1.0, "Live online class": .85, "Study-material download": 1.5, "Assignment / quiz submission": .35}[config.scenario]
    demand = config.workload_mbps * scenario_factor
    rtt = config.rtt_ms / 1000
    max_by_link = max(1, int(capacity * 1_000_000 * rtt / (config.mss_bytes * 8)))
    rows = []
    while elapsed < config.duration_seconds:
        dt = min(rtt, config.duration_seconds - elapsed)
        cwnd_start = cwnd
        offered = max(1, math.ceil(demand * 1_000_000 * dt / (config.mss_bytes * 8)))
        attempted = max(1, min(math.ceil(cwnd), max_by_link, offered))
        lost = sum(1 for _ in range(attempted) if rng.random() < p_loss)
        delivered = attempted - lost
        loss_event = lost > 0
        recovery = "none"
        if loss_event:
            event_id += 1
            dup_ack = attempted >= 4 and rng.random() < .65
            ssthresh = max(2.0, cwnd / 2.0)
            if algo == "Tahoe":
                cwnd = 1.0
                recovery = "fast_retransmit_then_slow_start" if dup_ack else "timeout"
            elif dup_ack:
                cwnd = ssthresh + 3.0
                recovery = "fast_retransmit_fast_recovery"
            else:
                cwnd = 1.0
                recovery = "timeout"
        elif cwnd < ssthresh:
            cwnd += max(1.0, cwnd)  # approximate exponential increase per RTT
        else:
            cwnd += 1.0 / max(cwnd, 1.0)  # approximate additive increase
        cwnd = max(1.0, min(float(cwnd), 10000.0))
        ssthresh = max(2.0, min(float(ssthresh), 10000.0))
        rows.append({
            "time_seconds": round(elapsed + dt, 4), "algorithm": algo,
            "cwnd_mss": round(cwnd_start, 4), "ssthresh_mss": round(ssthresh, 4),
            "segments_attempted": attempted, "segments_lost": lost,
            "segments_delivered": delivered, "loss_event": bool(loss_event),
            "loss_event_id": event_id if loss_event else None, "recovery_type": recovery,
            "sent_bytes": attempted * config.mss_bytes, "delivered_bytes": delivered * config.mss_bytes,
            "interval_seconds": dt, "effective_capacity_mbps": capacity,
            "workload_demand_mbps": demand, "estimated_rtt_ms": config.rtt_ms,
        })
        elapsed += dt
    return rows
