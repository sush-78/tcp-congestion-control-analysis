# Project Synopsis
**Title:** TCP Congestion Control Analysis for E-Learning Applications Using Python

**Domain:** Computer Networks and Python application development.

**Problem:** Static explanations do not always allow students to vary network conditions and inspect congestion-window behavior interactively.

**Proposed solution:** A local Streamlit dashboard simulates textbook TCP Tahoe and Reno for recorded lectures, live classes, study-material downloads, and assignment/quiz submissions. Users configure duration, RTT, bandwidth, packet-loss probability, congestion preset, workload, and random seed. The dashboard plots congestion window, throughput, and packet loss, displays summary metrics, and exports CSV.

**Tools:** Python, Streamlit, Matplotlib, Pandas, NumPy, pytest.

**Limitation:** Outputs are simulated estimates, not measurements from a real e-learning service or network.
