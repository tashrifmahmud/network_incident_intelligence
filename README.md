# Network Incident Intelligence

AI-assisted telecom incident analysis for root cause prediction, alarm pattern learning, and service assurance prototyping.

## Overview

This project is a synthetic but realistic telecom service assurance prototype built to explore how machine learning can support:

- root cause classification
- alarm correlation analysis
- AI-assisted troubleshooting
- incident prioritization

The project simulates a telecom operations environment with services, devices, incidents, and alarm sequences. A machine learning model is trained on incident-level features derived from alarm behavior and service impact patterns.

## Why this project

Telecom service assurance teams often deal with large volumes of alarms across multiple devices, technologies, and vendors. The challenge is not just detecting faults, but quickly understanding:

- what the likely root cause is
- how many customers or sites are impacted
- which incidents need urgent attention
- what troubleshooting action should happen next

This project is a small prototype built around that idea.

## Dataset Design

The dataset is synthetic because real telecom network data is private. However, it was designed using domain-informed root cause patterns.

### Files

- `services.csv`  
  Customer-facing services with service type, customer segment, and SLA tier

- `devices.csv`  
  Network inventory with device type, vendor, technology, region, and site mapping

- `incidents.csv`  
  Service-impacting incidents with root cause, priority, impact counts, and status

- `alarms.csv`  
  Alarm event sequences linked to incidents and devices

- `incident_features.csv`  
  Incident-level machine learning features derived from alarm behavior

## Simulated Root Causes

The dataset includes these root causes:

- `fiber_cut`
- `power_failure`
- `router_failure`
- `configuration_error`
- `congestion`
- `software_bug`

Each root cause has its own alarm behavior pattern, severity mix, likely device types, and impact profile.

## ML Approach

The first model in this project is a root cause classification model.

### Input features

- alarm type counts
- severity counts
- total alarm count
- unique device count
- unique vendor count
- unique technology count
- customer impact count
- site impact count
- region
- incident priority

### Output

- predicted root cause

### Model

- Random Forest Classifier

## Current Result

On the synthetic dataset, the first root cause classification model achieved strong accuracy because the data contains structured root-cause patterns.

Example result from the current version:

- Accuracy: `0.9667`

This is useful as a prototype, but real telecom production data would likely be much noisier and more difficult.

## Streamlit Demo

The project includes a Streamlit interface where a user can:

- choose a preset incident scenario
- adjust alarm and impact values
- predict the likely root cause
- view model confidence
- see suggested troubleshooting steps

Run the app with:

```bash
streamlit run app.py
```

## Project Structure

network_incident_intelligence/
│
├── data/
│   ├── services.csv
│   ├── devices.csv
│   ├── incidents.csv
│   ├── alarms.csv
│   ├── incident_features.csv
│   ├── root_cause_model.pkl
│   └── model_features.pkl
│
├── src/
│   ├── generate_base_data.py
│   ├── generate_incidents.py
│   ├── generate_alarms.py
│   ├── build_incident_features.py
│   ├── train_root_cause_model.py
│   └── predict_root_cause.py
│
├── app.py
├── dataset_plan.md
├── root_cause_patterns.md
├── data_dictionary.md
├── requirements.txt
└── README.md

## How to Run

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Generate the synthetic dataset
```bash
python src/generate_base_data.py
python src/generate_incidents.py
python src/generate_alarms.py
python src/build_incident_features.py
```

3. Train the model
```bash
python src/train_root_cause_model.py
```

4. Run a simple prediction script
```bash
python src/predict_root_cause.py
```
5. Launch the Streamlit app
```bash
streamlit run app.py
```
## Future Improvements

Possible next steps:

- incident clustering from raw alarms
- priority scoring model
- better alarm sequence modeling
- LLM-generated incident summaries
- explainable AI for NOC analysts
- richer multi-service and multi-site simulation

## Notes
This project is intended as a portfolio prototype for telecom AI and service assurance use cases. It is not trained on real production network data.