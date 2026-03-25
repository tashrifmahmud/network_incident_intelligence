import random
from datetime import timedelta
import pandas as pd

random.seed(42)

ROOT_CAUSE_PATTERNS = {
    "fiber_cut": {
        "alarm_types": ["link_down", "device_unreachable", "service_degraded", "packet_loss"],
        "severities": ["critical", "major"],
        "device_types": ["fiber_hub", "router", "gateway", "switch"],
        "alarm_count_range": (6, 12),
    },
    "power_failure": {
        "alarm_types": ["power_alarm", "device_unreachable", "service_degraded", "link_down"],
        "severities": ["critical", "major"],
        "device_types": ["base_station", "gateway", "router", "core_node"],
        "alarm_count_range": (5, 10),
    },
    "router_failure": {
        "alarm_types": ["device_unreachable", "link_down", "cpu_high", "memory_high"],
        "severities": ["critical", "major"],
        "device_types": ["router", "core_node", "gateway"],
        "alarm_count_range": (4, 8),
    },
    "configuration_error": {
        "alarm_types": ["config_mismatch", "service_degraded", "latency_high", "packet_loss"],
        "severities": ["major", "minor"],
        "device_types": ["router", "switch", "gateway", "core_node"],
        "alarm_count_range": (4, 7),
    },
    "congestion": {
        "alarm_types": ["latency_high", "packet_loss", "utilization_high", "cpu_high"],
        "severities": ["major", "minor"],
        "device_types": ["base_station", "router", "gateway", "switch"],
        "alarm_count_range": (4, 7),
    },
    "software_bug": {
        "alarm_types": ["service_degraded", "cpu_high", "memory_high", "packet_loss", "latency_high"],
        "severities": ["major", "minor"],
        "device_types": ["core_node", "gateway", "router", "base_station"],
        "alarm_count_range": (4, 8),
    },
}

ALARM_TEXT_MAP = {
    "link_down": "Link down detected on uplink interface",
    "device_unreachable": "Device is not reachable by network management system",
    "service_degraded": "Service quality degradation detected",
    "packet_loss": "Packet loss threshold exceeded",
    "power_alarm": "Power supply issue detected at site",
    "cpu_high": "CPU utilization exceeded threshold",
    "memory_high": "Memory utilization exceeded threshold",
    "latency_high": "Latency threshold exceeded",
    "utilization_high": "Interface utilization exceeded threshold",
    "config_mismatch": "Configuration mismatch detected against expected baseline",
}


def generate_alarms():
    incidents_df = pd.read_csv("data/incidents.csv", parse_dates=["incident_start_time", "incident_end_time"])
    devices_df = pd.read_csv("data/devices.csv")

    alarms = []
    alarm_counter = 1

    for _, incident in incidents_df.iterrows():
        incident_id = incident["incident_id"]
        service_id = incident["service_id"]
        root_cause = incident["root_cause"]
        start_time = incident["incident_start_time"]

        pattern = ROOT_CAUSE_PATTERNS[root_cause]

        service_devices = devices_df[devices_df["service_id"] == service_id]
        eligible_devices = service_devices[service_devices["device_type"].isin(pattern["device_types"])]

        if eligible_devices.empty:
            eligible_devices = service_devices

        num_alarms = random.randint(*pattern["alarm_count_range"])

        sampled_devices = eligible_devices.sample(
            n=min(num_alarms, len(eligible_devices)),
            replace=(len(eligible_devices) < num_alarms),
            random_state=None
        ).reset_index(drop=True)

        for i in range(num_alarms):
            alarm_id = f"ALM{alarm_counter:06d}"

            device = sampled_devices.iloc[i % len(sampled_devices)]
            alarm_type = random.choice(pattern["alarm_types"])
            severity = random.choice(pattern["severities"])

            timestamp = start_time + timedelta(seconds=random.randint(0, 900))

            acknowledged = random.choice([True, False])
            cleared = random.choice([True, False])

            alarms.append({
                "alarm_id": alarm_id,
                "incident_id": incident_id,
                "timestamp": timestamp,
                "device_id": device["device_id"],
                "alarm_type": alarm_type,
                "severity": severity,
                "alarm_text": ALARM_TEXT_MAP[alarm_type],
                "vendor": device["vendor"],
                "technology": device["technology"],
                "acknowledged": acknowledged,
                "cleared": cleared,
            })

            alarm_counter += 1

    return pd.DataFrame(alarms)


def main():
    alarms_df = generate_alarms()
    alarms_df.to_csv("data/alarms.csv", index=False)

    print("Generated alarms.csv")
    print(f"Alarms: {len(alarms_df)}")


if __name__ == "__main__":
    main()