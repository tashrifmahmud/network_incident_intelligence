import joblib
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Network Incident Intelligence", layout="wide")

TROUBLESHOOTING_MAP = {
    "fiber_cut": [
        "Check physical fiber path",
        "Verify optical link state",
        "Check nearby devices for connectivity loss",
    ],
    "power_failure": [
        "Verify site power status",
        "Check backup battery or power supply",
        "Confirm whether multiple devices at the site are down",
    ],
    "router_failure": [
        "Check device reachability",
        "Review CPU and memory status",
        "Inspect hardware health and recent failures",
    ],
    "configuration_error": [
        "Review recent configuration changes",
        "Compare expected and actual config state",
        "Consider rollback if issue started after a change",
    ],
    "congestion": [
        "Check traffic utilization",
        "Review peak-hour usage pattern",
        "Consider load balancing or capacity expansion",
    ],
    "software_bug": [
        "Review recent software release history",
        "Check repeating CPU or memory issues",
        "Escalate to engineering if pattern repeats",
    ],
}

SCENARIOS = {
    "Fiber Cut": {
        "customer_impact_count": 1800,
        "site_impact_count": 5,
        "total_alarm_count": 8,
        "unique_device_count": 4,
        "unique_vendor_count": 2,
        "unique_technology_count": 2,
        "link_down": 3,
        "packet_loss": 1,
        "service_degraded": 1,
        "device_unreachable": 2,
        "power_alarm": 0,
        "config_mismatch": 0,
        "latency_high": 1,
        "utilization_high": 0,
        "cpu_high": 0,
        "memory_high": 0,
        "critical": 4,
        "major": 3,
        "minor": 1,
        "region": "Toronto",
        "priority": "critical",
    },
    "Power Failure": {
        "customer_impact_count": 2200,
        "site_impact_count": 4,
        "total_alarm_count": 7,
        "unique_device_count": 4,
        "unique_vendor_count": 1,
        "unique_technology_count": 1,
        "link_down": 1,
        "packet_loss": 0,
        "service_degraded": 1,
        "device_unreachable": 3,
        "power_alarm": 2,
        "config_mismatch": 0,
        "latency_high": 0,
        "utilization_high": 0,
        "cpu_high": 0,
        "memory_high": 0,
        "critical": 4,
        "major": 2,
        "minor": 1,
        "region": "Mississauga",
        "priority": "critical",
    },
    "Congestion": {
        "customer_impact_count": 450,
        "site_impact_count": 2,
        "total_alarm_count": 6,
        "unique_device_count": 3,
        "unique_vendor_count": 2,
        "unique_technology_count": 2,
        "link_down": 0,
        "packet_loss": 2,
        "service_degraded": 1,
        "device_unreachable": 0,
        "power_alarm": 0,
        "config_mismatch": 0,
        "latency_high": 2,
        "utilization_high": 2,
        "cpu_high": 1,
        "memory_high": 0,
        "critical": 0,
        "major": 4,
        "minor": 2,
        "region": "Ottawa",
        "priority": "medium",
    },
    "Configuration Error": {
        "customer_impact_count": 180,
        "site_impact_count": 1,
        "total_alarm_count": 5,
        "unique_device_count": 2,
        "unique_vendor_count": 1,
        "unique_technology_count": 1,
        "link_down": 0,
        "packet_loss": 1,
        "service_degraded": 2,
        "device_unreachable": 0,
        "power_alarm": 0,
        "config_mismatch": 2,
        "latency_high": 1,
        "utilization_high": 0,
        "cpu_high": 0,
        "memory_high": 0,
        "critical": 0,
        "major": 3,
        "minor": 2,
        "region": "Brampton",
        "priority": "medium",
    },
}


@st.cache_resource
def load_model():
    model = joblib.load("data/root_cause_model.pkl")
    expected_features = joblib.load("data/model_features.pkl")
    return model, expected_features


def align_features(input_df, expected_features):
    for col in expected_features:
        if col not in input_df.columns:
            input_df[col] = 0
    return input_df[expected_features]


st.title("Network Incident Intelligence")
st.caption("AI-assisted root cause prediction for telecom service assurance")

model, expected_features = load_model()

st.sidebar.header("Scenario Presets")
selected_scenario = st.sidebar.selectbox(
    "Choose a sample incident",
    list(SCENARIOS.keys())
)

preset = SCENARIOS[selected_scenario]

st.sidebar.write("Load a preset, then adjust values in the main panel.")

st.subheader("Incident Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Customer Impact", preset["customer_impact_count"])
m2.metric("Impacted Sites", preset["site_impact_count"])
m3.metric("Alarm Volume", preset["total_alarm_count"])
m4.metric("Devices Affected", preset["unique_device_count"])

st.subheader("Incident Input")

col1, col2, col3 = st.columns(3)

with col1:
    customer_impact_count = st.number_input("Customer Impact Count", min_value=0, value=preset["customer_impact_count"])
    site_impact_count = st.number_input("Site Impact Count", min_value=0, value=preset["site_impact_count"])
    total_alarm_count = st.number_input("Total Alarm Count", min_value=0, value=preset["total_alarm_count"])
    unique_device_count = st.number_input("Unique Device Count", min_value=0, value=preset["unique_device_count"])
    unique_vendor_count = st.number_input("Unique Vendor Count", min_value=0, value=preset["unique_vendor_count"])
    unique_technology_count = st.number_input("Unique Technology Count", min_value=0, value=preset["unique_technology_count"])

with col2:
    link_down = st.number_input("link_down", min_value=0, value=preset["link_down"])
    packet_loss = st.number_input("packet_loss", min_value=0, value=preset["packet_loss"])
    service_degraded = st.number_input("service_degraded", min_value=0, value=preset["service_degraded"])
    device_unreachable = st.number_input("device_unreachable", min_value=0, value=preset["device_unreachable"])
    power_alarm = st.number_input("power_alarm", min_value=0, value=preset["power_alarm"])
    config_mismatch = st.number_input("config_mismatch", min_value=0, value=preset["config_mismatch"])
    latency_high = st.number_input("latency_high", min_value=0, value=preset["latency_high"])
    utilization_high = st.number_input("utilization_high", min_value=0, value=preset["utilization_high"])
    cpu_high = st.number_input("cpu_high", min_value=0, value=preset["cpu_high"])
    memory_high = st.number_input("memory_high", min_value=0, value=preset["memory_high"])

with col3:
    critical = st.number_input("Critical alarms", min_value=0, value=preset["critical"])
    major = st.number_input("Major alarms", min_value=0, value=preset["major"])
    minor = st.number_input("Minor alarms", min_value=0, value=preset["minor"])

    region = st.selectbox("Region", ["Toronto", "Mississauga", "Ottawa", "Brampton"],
                          index=["Toronto", "Mississauga", "Ottawa", "Brampton"].index(preset["region"]))
    priority = st.selectbox("Priority", ["low", "medium", "high", "critical"],
                            index=["low", "medium", "high", "critical"].index(preset["priority"]))

if st.button("Predict Root Cause", use_container_width=True):
    input_data = {
        "customer_impact_count": customer_impact_count,
        "site_impact_count": site_impact_count,
        "total_alarm_count": total_alarm_count,
        "unique_device_count": unique_device_count,
        "unique_vendor_count": unique_vendor_count,
        "unique_technology_count": unique_technology_count,
        "link_down": link_down,
        "packet_loss": packet_loss,
        "service_degraded": service_degraded,
        "device_unreachable": device_unreachable,
        "power_alarm": power_alarm,
        "config_mismatch": config_mismatch,
        "latency_high": latency_high,
        "utilization_high": utilization_high,
        "cpu_high": cpu_high,
        "memory_high": memory_high,
        "critical": critical,
        "major": major,
        "minor": minor,
        "region_Toronto": 1 if region == "Toronto" else 0,
        "region_Mississauga": 1 if region == "Mississauga" else 0,
        "region_Ottawa": 1 if region == "Ottawa" else 0,
        "region_Brampton": 1 if region == "Brampton" else 0,
        "priority_low": 1 if priority == "low" else 0,
        "priority_medium": 1 if priority == "medium" else 0,
        "priority_high": 1 if priority == "high" else 0,
        "priority_critical": 1 if priority == "critical" else 0,
    }

    input_df = pd.DataFrame([input_data])
    input_df = align_features(input_df, expected_features)

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    class_names = model.classes_
    prob_df = pd.DataFrame({
        "Root Cause": class_names,
        "Probability": probabilities
    }).sort_values(by="Probability", ascending=False)

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Prediction Result")
        st.success(f"Predicted Root Cause: {prediction}")
        st.metric("Confidence", f"{confidence:.2%}")

        st.subheader("Suggested Troubleshooting")
        for step in TROUBLESHOOTING_MAP[prediction]:
            st.write(f"- {step}")

    with right:
        st.subheader("Class Probabilities")
        st.dataframe(
            prob_df.style.format({"Probability": "{:.2%}"}),
            use_container_width=True
        )