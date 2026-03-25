import pandas as pd


def build_incident_features():
    incidents_df = pd.read_csv("data/incidents.csv")
    alarms_df = pd.read_csv("data/alarms.csv")

    # Count alarm types per incident
    alarm_type_counts = pd.crosstab(alarms_df["incident_id"], alarms_df["alarm_type"])
    alarm_type_counts = alarm_type_counts.reset_index()

    # Count severities per incident
    severity_counts = pd.crosstab(alarms_df["incident_id"], alarms_df["severity"])
    severity_counts = severity_counts.reset_index()

    # Count total alarms per incident
    total_alarm_counts = alarms_df.groupby("incident_id").size().reset_index(name="total_alarm_count")

    # Count unique devices affected per incident
    unique_device_counts = alarms_df.groupby("incident_id")["device_id"].nunique().reset_index(name="unique_device_count")

    # Count unique vendors affected per incident
    unique_vendor_counts = alarms_df.groupby("incident_id")["vendor"].nunique().reset_index(name="unique_vendor_count")

    # Count unique technologies affected per incident
    unique_tech_counts = alarms_df.groupby("incident_id")["technology"].nunique().reset_index(name="unique_technology_count")

    # Merge all incident-level alarm features
    features_df = incidents_df.merge(total_alarm_counts, on="incident_id", how="left")
    features_df = features_df.merge(unique_device_counts, on="incident_id", how="left")
    features_df = features_df.merge(unique_vendor_counts, on="incident_id", how="left")
    features_df = features_df.merge(unique_tech_counts, on="incident_id", how="left")
    features_df = features_df.merge(alarm_type_counts, on="incident_id", how="left")
    features_df = features_df.merge(severity_counts, on="incident_id", how="left")

    # Fill missing counts with 0
    count_columns = features_df.columns.difference([
        "incident_id",
        "incident_start_time",
        "incident_end_time",
        "region",
        "site_id",
        "service_id",
        "root_cause",
        "priority",
        "ticket_status"
    ])

    features_df[count_columns] = features_df[count_columns].fillna(0)

    return features_df


def main():
    features_df = build_incident_features()
    features_df.to_csv("data/incident_features.csv", index=False)

    print("Generated incident_features.csv")
    print(f"Rows: {len(features_df)}")
    print(f"Columns: {len(features_df.columns)}")


if __name__ == "__main__":
    main()