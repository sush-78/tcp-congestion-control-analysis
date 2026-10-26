# TCP Congestion Control Analysis for E-Learning Applications

Interactive educational simulation of textbook TCP Tahoe and TCP Reno using Python and Streamlit.

## Windows setup
Open this folder in VS Code and run each command separately:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

## Start the website
```powershell
python -m streamlit run app.py
```

## Run tests
```powershell
python -m pytest -q
```

## Files
- `app.py`: interactive dashboard, plots, tables, CSV downloads.
- `simulator.py`: parameter validation and seeded Tahoe/Reno simulation.
- `metrics.py`: throughput, packet loss, delivered data, and delay estimate.
- `experiments.py`: repeatable experiment presets and comparison.
- `report/`: report, synopsis, architecture, presentation/viva material.
- `tests/`: automated checks.

## Accuracy note
This is a simplified discrete-round educational model. It does not send real TCP packets or measure a real e-learning platform. ACK/loss detection and Reno recovery are approximated. Use actual application output in the final report.
