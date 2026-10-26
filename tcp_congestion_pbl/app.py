"""Interactive Streamlit dashboard for TCP congestion-control education."""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from simulator import SimulationConfig, run_simulation
from metrics import calculate_metrics
from experiments import EXPERIMENT_PRESETS, run_preset_experiment

st.set_page_config(page_title="TCP Congestion Lab", page_icon="🌐", layout="wide")
st.markdown("""
<style>
.main .block-container{padding-top:1.4rem;max-width:1500px}
.hero{padding:1.5rem 1.7rem;border-radius:18px;background:linear-gradient(120deg,#102a43,#176b87);color:white;margin-bottom:1rem}
.hero h1{color:white;margin-bottom:.25rem}.hero p{font-size:1.05rem}
</style>
<div class="hero"><h1>TCP Congestion Control Lab</h1><p>Explore how simulated network conditions affect e-learning traffic using textbook TCP Tahoe and TCP Reno.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Simulation controls")
    scenario = st.selectbox("E-learning scenario", ["Recorded video lecture", "Live online class", "Study-material download", "Assignment / quiz submission"])
    algorithm = st.selectbox("TCP algorithm", ["Reno", "Tahoe"])
    duration = st.slider("Duration (seconds)", 5, 120, 30)
    rtt = st.slider("Round-trip time (ms)", 10, 500, 100)
    bandwidth = st.slider("Link bandwidth (Mbps)", 1.0, 100.0, 5.0, 1.0)
    loss = st.slider("Packet-loss probability (%)", 0.0, 30.0, 2.0, 0.5)
    congestion = st.select_slider("Network congestion", ["Low", "Medium", "High"], value="Medium")
    workload = st.slider("Base workload demand (Mbps)", 0.1, 20.0, 3.0, 0.1)
    initial_cwnd = st.slider("Initial cwnd (MSS)", 1, 20, 1)
    ssthresh = st.slider("Initial ssthresh (MSS)", 2, 100, 16)
    seed = st.number_input("Random seed", min_value=0, max_value=2_147_483_647, value=42, step=1)
    run_clicked = st.button("▶ Run simulation", type="primary", use_container_width=True)
    st.caption("Simulated results only; no live network is measured.")

cfg = SimulationConfig(duration_seconds=duration, rtt_ms=float(rtt), bandwidth_mbps=float(bandwidth), packet_loss_pct=float(loss), initial_cwnd=float(initial_cwnd), initial_ssthresh=float(ssthresh), seed=int(seed), congestion_level=congestion, scenario=scenario, workload_mbps=float(workload), algorithm=algorithm)
if "records" not in st.session_state: st.session_state.records = None
if run_clicked or st.session_state.records is None:
    try:
        st.session_state.records = run_simulation(cfg, algorithm)
        st.session_state.metrics = calculate_metrics(st.session_state.records, duration)
        st.session_state.active_cfg = cfg
    except (ValueError, RuntimeError) as exc: st.error(f"Simulation failed: {exc}")

if st.session_state.records is not None:
    records, m, active = st.session_state.records, st.session_state.metrics, st.session_state.active_cfg
    dash, exp, about = st.tabs(["Dashboard", "Experiments", "Model & assumptions"])
    with dash:
        st.caption(f"Scenario: **{active.scenario}** · TCP **{active.algorithm}** · Seed **{active.seed}**")
        cols = st.columns(4)
        cards = [("Average throughput", f"{m['average_throughput_mbps']:.3f} Mbps"), ("Packet-loss rate", f"{m['packet_loss_rate_pct']:.2f}%"), ("Loss events", str(m["loss_events"])), ("Average cwnd", f"{m['average_cwnd_mss']:.2f} MSS")]
        for col, (label, value) in zip(cols, cards): col.metric(label, value)
        c2 = st.columns(3)
        c2[0].metric("Delivered data", f"{m['successfully_delivered_mb']:.3f} MB")
        c2[1].metric("Estimated transmission delay", f"{m['estimated_transmission_delay_ms']:.2f} ms")
        c2[2].metric("Segments attempted", f"{m['attempted_segments']:,}")
        df = pd.DataFrame(records)
        st.subheader("Congestion window vs time")
        fig, ax = plt.subplots(figsize=(10, 3.6)); ax.plot(df.time_seconds, df.cwnd_mss, label="cwnd", linewidth=2); ax.plot(df.time_seconds, df.ssthresh_mss, label="ssthresh", linestyle="--"); ax.set(xlabel="Simulation time (s)", ylabel="Window (MSS)"); ax.grid(alpha=.25); ax.legend(); st.pyplot(fig); plt.close(fig)
        df["interval_throughput_mbps"] = df.delivered_bytes * 8 / df.interval_seconds / 1_000_000
        st.subheader("Throughput vs time")
        fig, ax = plt.subplots(figsize=(10, 3)); ax.plot(df.time_seconds, df.interval_throughput_mbps); ax.set(xlabel="Simulation time (s)", ylabel="Delivered throughput (Mbps)"); ax.grid(alpha=.25); st.pyplot(fig); plt.close(fig)
        st.subheader("Packet loss vs time")
        fig, ax = plt.subplots(figsize=(10, 2.8)); ax.bar(df.time_seconds, df.segments_lost, width=max(.05, active.rtt_ms/1000*.75)); ax.set(xlabel="Simulation time (s)", ylabel="Lost segment transmissions"); ax.grid(axis="y", alpha=.25); st.pyplot(fig); plt.close(fig)
        st.subheader("Simulation results table")
        display_cols = ["time_seconds", "algorithm", "cwnd_mss", "ssthresh_mss", "segments_attempted", "segments_lost", "segments_delivered", "loss_event", "recovery_type", "delivered_bytes"]
        st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        st.download_button("⬇ Download results as CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"tcp_{active.algorithm.lower()}_results.csv", mime="text/csv")
    with exp:
        st.subheader("Predefined reproducible experiments")
        preset = st.selectbox("Experiment preset", list(EXPERIMENT_PRESETS) + ["Tahoe vs Reno"])
        if st.button("Run comparison", type="primary"): st.session_state.exp_df = run_preset_experiment(cfg, preset)
        if "exp_df" in st.session_state:
            exp_df = st.session_state.exp_df
            st.dataframe(exp_df, use_container_width=True, hide_index=True)
            fig, ax = plt.subplots(figsize=(7, 3)); ax.bar(exp_df.algorithm, exp_df.average_throughput_mbps); ax.set(ylabel="Average throughput (Mbps)", title=preset); ax.grid(axis="y", alpha=.25); st.pyplot(fig); plt.close(fig)
            st.download_button("Download experiment summary CSV", exp_df.to_csv(index=False).encode("utf-8"), file_name="tcp_experiment_comparison.csv", mime="text/csv")
    with about:
        st.subheader("Definitions")
        st.markdown("""
- **cwnd:** sender congestion window, in maximum segment sizes (MSS).
- **ssthresh:** threshold between slow start and congestion avoidance.
- **Throughput:** successfully delivered payload bits divided by simulation duration, converted to Mbps.
- **Packet-loss rate:** lost segment transmissions divided by attempted transmissions.
- **Loss event:** a round containing one or more lost segments.
- **Estimated transmission delay:** configured RTT plus simplified serialization delay; it is not measured end-to-end delay.
- **Reproducibility:** the seed repeats pseudo-random outcomes for the same configuration.
        """)
        st.warning("Educational approximation only. ACK processing, retransmission timers, queues, receiver windows, pacing, and modern TCP variants are not fully modeled. Reno fast recovery is an abstraction for learning.")
        st.json({"duration_seconds": active.duration_seconds, "rtt_ms": active.rtt_ms, "bandwidth_mbps": active.bandwidth_mbps, "packet_loss_pct": active.packet_loss_pct, "congestion_level": active.congestion_level, "scenario": active.scenario, "seed": active.seed})
