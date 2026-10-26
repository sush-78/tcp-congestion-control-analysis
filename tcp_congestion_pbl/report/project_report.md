# TCP Congestion Control Analysis for E-Learning Applications Using Python

> Draft report. Replace placeholders and add screenshots and experimental values only after running the application.

## 1. Title Page
**Student:** [Student name]  
**Department:** Computer Science and Engineering  
**Institution:** [College name]  
**Academic year:** [Academic year]

## 2. Abstract
This project presents an educational Python simulation for studying textbook TCP Tahoe and TCP Reno under configurable network conditions relevant to e-learning workloads. A Streamlit dashboard allows users to select simulated traffic scenarios and adjust round-trip time, bandwidth, packet-loss probability, congestion level, workload, and duration. The application records congestion-window behavior and derives throughput, loss rate, delivered payload, loss-event counts, and a simplified delay estimate. Matplotlib visualizations and CSV exports support repeatable experiments. The application does not measure a live network; outputs depend on the documented model.

## 3. Introduction
Online education depends on network communication for live classes, video playback, downloads, and assessments. TCP congestion control influences how a sender adjusts transmission in response to network feedback. An interactive simulation helps students explore these concepts.

## 4. Problem Statement
Static diagrams do not always allow students to vary network conditions interactively. This project provides a local dashboard to observe simulated congestion-window changes and compare Tahoe and Reno.

## 5. Objectives
- Implement educational Tahoe and Reno congestion-window models.
- Vary simulated RTT, bandwidth, packet loss, congestion, and workload.
- Calculate and plot metrics from recorded simulation values.
- Support reproducible experiments and CSV export.

## 6. Existing System
Textbook explanations and static figures are common learning methods. This project adds a local interactive simulation; this is a project motivation, not a claim that all existing tools lack such features.

## 7. Proposed System
A local Streamlit application runs seeded simulations, calculates metrics, visualizes time-series data, and exports CSV. No paid API, cloud service, login, or database is required.

## 8. Literature Review and TCP Background
TCP uses a congestion window (`cwnd`) to regulate unacknowledged data. Slow start grows the window rapidly, while congestion avoidance grows it more gradually. Classic Tahoe reduces the threshold and returns `cwnd` to one MSS after loss. Classic Reno can use fast retransmit and fast recovery for triple-duplicate-ACK-like loss detection, while timeout recovery returns to slow start. Real behavior depends on the TCP implementation and network stack.

## 9. System Requirements
Python 3.10+, Streamlit, Matplotlib, Pandas, NumPy, pytest, and a modern browser. Internet is needed for initial package installation only.

## 10. System Architecture
User configuration → simulation engine → per-round records → metric calculation → dashboard graphs, tables, and CSV export.

## 11. Methodology and Algorithm Design
The model advances in RTT-sized steps. A seeded random generator samples per-segment loss. Effective capacity depends on the congestion preset. The model updates `cwnd` and `ssthresh` according to the selected textbook variant and records each round. It is not a full TCP/IP stack.

## 12. Implementation Details
`simulator.py` validates configuration and simulates Tahoe/Reno; `metrics.py` calculates summary metrics; `experiments.py` defines comparison presets; `app.py` builds the Streamlit UI; `tests/` contains automated checks.

## 13. Experimental Setup
Record software versions, scenario, seed, RTT, bandwidth, loss probability, congestion level, and duration. Compare algorithms with matching settings. Repeat with multiple seeds before making broad claims.

## 14. Results and Graph Analysis
**Placeholder:** Insert screenshots and values from actual runs. Test low, medium, and high congestion; low and high loss; and Tahoe versus Reno. Explain only observed results and note model limitations.

## 15. Limitations
- Simplified discrete RTT rounds and ACK/loss detection.
- No real packet transmission or live network measurement.
- No full retransmission timer, receive window, queue, pacing, or modern TCP implementation.
- Workload multipliers are illustrative assumptions.
- Results depend on parameters and random seed.

## 16. Conclusion
The application provides a local educational environment for exploring congestion-window dynamics and model-derived metrics. Final conclusions should be based on actual experiments with the completed application.

## 17. Future Enhancements
Add detailed ACK and retransmission modeling, repeated-seed statistical summaries, and comparisons with controlled packet traces.

## 18. References
1. W. Stevens, “TCP Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Algorithms,” RFC 2001, 1997. https://www.rfc-editor.org/rfc/rfc2001
2. M. Allman, V. Paxson, and W. Stevens, “TCP Congestion Control,” RFC 2581, 1999. https://www.rfc-editor.org/rfc/rfc2581
3. M. Allman, V. Paxson, and E. Blanton, “TCP Congestion Control,” RFC 5681, 2009. https://www.rfc-editor.org/rfc/rfc5681
4. Streamlit documentation: https://docs.streamlit.io/
5. Matplotlib documentation: https://matplotlib.org/stable/
