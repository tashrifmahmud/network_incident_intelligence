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


@st.cache_resource
def load_model():
    model = joblib.load("data/root_cause_model.pkl")
    expected_features = joblib.load("data/model_features.pkl")
    return model, expected_features


def align_features(input_df, expected_features):
    for col in expected_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_features]
    return input_df


st.title("Network Incident Intelligence")
st.write("AI-assisted root cause prediction for telecom network incidents.")

model, expected_features = load_model()

st.subheader("Incident Input")

col1, col2, col3 = st.columns(3)

with col1:
    customer_impact_count = st.number_input("Customer Impact Count", min_value=0, value=1800)
    site_impact_count = st.number_input("Site Impact Count", min_value=0, value=5)
    total_alarm_count = st.number_input("Total Alarm Count", min_value=0, value=8)
    unique_device_count = st.number_input("Unique Device Count", min_value=0, value=4)
    unique_vendor_count = st.number_input("Unique Vendor Count", min_value=0, value=2)
    unique_technology_count = st.number_input("Unique Technology Count", min_value=0, value=2)

with col2:
    link_down = st.number_input("link_down", min_value=0, value=3)
    packet_loss = st.number_input("packet_loss", min_value=0, value=1)
    service_degraded = st.number_input("service_degraded", min_value=0, value=1)
    device_unreachable = st.number_input("device_unreachable", min_value=0, value=2)
    power_alarm = st.number_input("power_alarm", min_value=0, value=0)
    config_mismatch = st.number_input("config_mismatch", min_value=0, value=0)
    latency_high = st.number_input("latency_high", min_value=0, value=1)
    utilization_high = st.number_input("utilization_high", min_value=0, value=0)
    cpu_high = st.number_input("cpu_high", min_value=0, value=0)
    memory_high = st.number_input("memory_high", min_value=0, value=0)

with col3:
    critical = st.number_input("Critical alarms", min_value=0, value=4)
    major = st.number_input("Major alarms", min_value=0, value=3)
    minor = st.number_input("Minor alarms", min_value=0, value=1)

    region = st.selectbox("Region", ["Toronto", "Mississauga", "Ottawa", "Brampton"])
    priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])


if st.button("Predict Root Cause"):
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

    st.subheader("Prediction Result")
    st.success(f"Predicted Root Cause: {prediction}")
    st.write(f"Confidence: {confidence:.2%}")

    st.subheader("Class Probabilities")
    st.dataframe(prob_df, use_container_width=True)

    st.subheader("Suggested Troubleshooting")
    for step in TROUBLESHOOTING_MAP[prediction]:
        st.write(f"- {step}")