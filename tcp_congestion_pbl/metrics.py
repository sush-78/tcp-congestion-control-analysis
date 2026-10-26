"""Summary metrics derived from simulation records, not live measurements."""
import pandas as pd

def calculate_metrics(records, duration_seconds):
    if duration_seconds <= 0: raise ValueError("Duration must be greater than zero.")
    if not records: raise ValueError("Cannot calculate metrics from empty records.")
    df = pd.DataFrame(records)
    attempted, lost = int(df["segments_attempted"].sum()), int(df["segments_lost"].sum())
    delivered_bytes = int(df["delivered_bytes"].sum())
    throughput = delivered_bytes * 8 / duration_seconds / 1_000_000
    loss_rate = lost / attempted * 100 if attempted else 0.0
    capacity = float(df["effective_capacity_mbps"].iloc[0])
    rtt_ms = float(df["estimated_rtt_ms"].mean())
    serialization_ms = (float(df["sent_bytes"].mean()) * 8 / (capacity * 1_000_000) * 1000) if capacity > 0 else 0.0
    return {
        "average_throughput_mbps": round(throughput, 6), "packet_loss_rate_pct": round(loss_rate, 4),
        "loss_events": int(df["loss_event"].sum()), "average_cwnd_mss": round(float(df["cwnd_mss"].mean()), 4),
        "estimated_transmission_delay_ms": round(rtt_ms + serialization_ms, 4),
        "successfully_delivered_bytes": delivered_bytes, "successfully_delivered_mb": round(delivered_bytes / 1_000_000, 6),
        "attempted_segments": attempted, "lost_segments": lost, "delivered_segments": int(df["segments_delivered"].sum()),
    }
