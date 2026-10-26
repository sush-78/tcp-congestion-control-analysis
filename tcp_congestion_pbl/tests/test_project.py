import pytest
from simulator import SimulationConfig, run_simulation
from metrics import calculate_metrics

def test_cwnd_and_threshold_valid():
    rows = run_simulation(SimulationConfig(duration_seconds=5, seed=7), "Tahoe")
    assert rows and all(r["cwnd_mss"] >= 1 and r["ssthresh_mss"] >= 2 for r in rows)

def test_reproducible_seed():
    cfg = SimulationConfig(duration_seconds=8, seed=123, packet_loss_pct=8)
    assert run_simulation(cfg, "Reno") == run_simulation(cfg, "Reno")

def test_tahoe_reno_loss_responses():
    cfg = SimulationConfig(duration_seconds=20, seed=2, packet_loss_pct=20)
    tahoe, reno = run_simulation(cfg, "Tahoe"), run_simulation(cfg, "Reno")
    assert any(r["recovery_type"] == "fast_retransmit_then_slow_start" for r in tahoe)
    assert any(r["recovery_type"] == "fast_retransmit_fast_recovery" for r in reno)

def test_throughput_units():
    cfg = SimulationConfig(duration_seconds=5, seed=4)
    rows = run_simulation(cfg, "Reno"); m = calculate_metrics(rows, 5)
    assert m["average_throughput_mbps"] == pytest.approx(m["successfully_delivered_bytes"] * 8 / 5 / 1_000_000)
    assert 0 <= m["packet_loss_rate_pct"] <= 100
    assert m["estimated_transmission_delay_ms"] > cfg.rtt_ms

def test_invalid_duration_rejected():
    with pytest.raises(ValueError): run_simulation(SimulationConfig(duration_seconds=0))

def test_records_have_csv_columns():
    row = run_simulation(SimulationConfig(duration_seconds=3))[0]
    assert {"time_seconds", "cwnd_mss", "ssthresh_mss", "segments_lost", "delivered_bytes"} <= set(row)
