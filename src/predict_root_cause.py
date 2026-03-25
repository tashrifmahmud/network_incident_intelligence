import joblib
import pandas as pd


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


def build_input_row():
    """
    Change these values to test different incident patterns.
    """
    sample_input = {
    "customer_impact_count": 2200,
    "site_impact_count": 4,
    "total_alarm_count": 7,
    "unique_device_count": 4,
    "unique_vendor_count": 1,
    "unique_technology_count": 1,

    "config_mismatch": 0,
    "cpu_high": 0,
    "device_unreachable": 3,
    "latency_high": 0,
    "link_down": 1,
    "memory_high": 0,
    "packet_loss": 0,
    "power_alarm": 2,
    "service_degraded": 1,
    "utilization_high": 0,

    "critical": 4,
    "major": 2,
    "minor": 1,

    "region_Brampton": 0,
    "region_Mississauga": 1,
    "region_Ottawa": 0,
    "region_Toronto": 0,

    "priority_critical": 1,
    "priority_high": 0,
    "priority_low": 0,
    "priority_medium": 0,
}

    return pd.DataFrame([sample_input])


def align_features(input_df, expected_features):
    for col in expected_features:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_features]
    return input_df


def main():
    model = joblib.load("data/root_cause_model.pkl")
    expected_features = joblib.load("data/model_features.pkl")

    input_df = build_input_row()
    input_df = align_features(input_df, expected_features)

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    class_names = model.classes_
    class_probs = dict(zip(class_names, probabilities))
    confidence = max(probabilities)

    print("\nPrediction Result")
    print("-" * 40)
    print(f"Predicted Root Cause: {prediction}")
    print(f"Confidence: {confidence:.2%}")

    print("\nClass Probabilities:")
    for class_name, prob in sorted(class_probs.items(), key=lambda x: x[1], reverse=True):
        print(f"{class_name}: {prob:.2%}")

    print("\nSuggested Troubleshooting:")
    for step in TROUBLESHOOTING_MAP[prediction]:
        print(f"- {step}")


if __name__ == "__main__":
    main()