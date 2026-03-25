import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

ROOT_CAUSES = [
    "fiber_cut",
    "power_failure",
    "router_failure",
    "configuration_error",
    "congestion",
    "software_bug",
]

PRIORITIES = ["low", "medium", "high", "critical"]

TICKET_STATUS = ["open", "in_progress", "resolved"]


def generate_incidents(num_incidents=300):

    services = pd.read_csv("data/services.csv")

    incidents = []

    base_time = datetime(2026, 3, 1)

    for i in range(1, num_incidents + 1):

        incident_id = f"INC{i:04d}"

        service = services.sample(1).iloc[0]

        service_id = service["service_id"]
        region = service["region"]

        root_cause = random.choice(ROOT_CAUSES)

        start_offset = random.randint(0, 1440)
        start_time = base_time + timedelta(minutes=start_offset)

        duration = random.randint(10, 120)
        end_time = start_time + timedelta(minutes=duration)

        if root_cause in ["fiber_cut", "power_failure"]:
            priority = "critical"
            customer_impact = random.randint(800, 5000)
            site_impact = random.randint(3, 10)

        elif root_cause in ["router_failure"]:
            priority = "high"
            customer_impact = random.randint(300, 2000)
            site_impact = random.randint(2, 6)

        elif root_cause in ["congestion"]:
            priority = "medium"
            customer_impact = random.randint(100, 800)
            site_impact = random.randint(1, 4)

        elif root_cause in ["configuration_error"]:
            priority = "medium"
            customer_impact = random.randint(50, 500)
            site_impact = random.randint(1, 3)

        else:
            priority = random.choice(PRIORITIES)
            customer_impact = random.randint(20, 400)
            site_impact = random.randint(1, 2)

        ticket_status = random.choice(TICKET_STATUS)

        incidents.append({
            "incident_id": incident_id,
            "incident_start_time": start_time,
            "incident_end_time": end_time,
            "region": region,
            "site_id": f"SITE{random.randint(1,120):03d}",
            "service_id": service_id,
            "root_cause": root_cause,
            "priority": priority,
            "customer_impact_count": customer_impact,
            "site_impact_count": site_impact,
            "ticket_status": ticket_status
        })

    return pd.DataFrame(incidents)


def main():

    incidents_df = generate_incidents()

    incidents_df.to_csv("data/incidents.csv", index=False)

    print("Generated incidents.csv")
    print(f"Incidents: {len(incidents_df)}")


if __name__ == "__main__":
    main()