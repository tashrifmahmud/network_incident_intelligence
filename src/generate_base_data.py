import os
import random
import pandas as pd

random.seed(42)

# -----------------------------
# Controlled values
# -----------------------------
REGIONS = ["Toronto", "Mississauga", "Ottawa", "Brampton"]

SERVICE_TYPES = ["Mobile Data", "Voice", "SMS", "Broadband", "Enterprise VPN"]
CUSTOMER_SEGMENTS = ["Consumer", "Business", "Enterprise"]
SLA_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]

DEVICE_TYPES = ["router", "switch", "base_station", "core_node", "gateway", "fiber_hub"]
VENDORS = ["Ericsson", "Nokia", "Huawei", "Cisco", "Juniper"]
TECHNOLOGIES = ["4G", "5G", "IP_MPLS", "Fiber", "Microwave"]

# Simple device-to-technology logic to make things more realistic
DEVICE_TECH_MAP = {
    "router": ["IP_MPLS", "Fiber"],
    "switch": ["IP_MPLS", "Fiber"],
    "base_station": ["4G", "5G", "Microwave"],
    "core_node": ["IP_MPLS", "5G"],
    "gateway": ["IP_MPLS", "Fiber", "5G"],
    "fiber_hub": ["Fiber"],
}


# -----------------------------
# Helpers
# -----------------------------
def ensure_data_folder():
    os.makedirs("data", exist_ok=True)


def generate_services(num_services=20):
    services = []

    for i in range(1, num_services + 1):
        service_id = f"SVC{i:03d}"
        region = random.choice(REGIONS)
        service_type = random.choice(SERVICE_TYPES)
        customer_segment = random.choice(CUSTOMER_SEGMENTS)
        sla_tier = random.choice(SLA_TIERS)

        service_name = f"{region} {service_type} Service {i}"

        services.append({
            "service_id": service_id,
            "service_name": service_name,
            "service_type": service_type,
            "customer_segment": customer_segment,
            "sla_tier": sla_tier,
            "region": region,
        })

    return pd.DataFrame(services)


def generate_devices(services_df, devices_per_service=6):
    devices = []
    device_counter = 1
    site_counter = 1

    for _, service in services_df.iterrows():
        service_id = service["service_id"]
        region = service["region"]

        for _ in range(devices_per_service):
            device_id = f"DEV{device_counter:04d}"
            site_id = f"SITE{site_counter:03d}"

            device_type = random.choice(DEVICE_TYPES)
            vendor = random.choice(VENDORS)
            technology = random.choice(DEVICE_TECH_MAP[device_type])

            device_name = f"{region[:3].upper()}-{device_type[:3].upper()}-{device_counter:02d}"

            devices.append({
                "device_id": device_id,
                "device_name": device_name,
                "device_type": device_type,
                "vendor": vendor,
                "technology": technology,
                "region": region,
                "site_id": site_id,
                "service_id": service_id,
            })

            device_counter += 1
            site_counter += 1

    return pd.DataFrame(devices)


def main():
    ensure_data_folder()

    services_df = generate_services(num_services=20)
    devices_df = generate_devices(services_df, devices_per_service=6)

    services_df.to_csv("data/services.csv", index=False)
    devices_df.to_csv("data/devices.csv", index=False)

    print("Generated:")
    print("- data/services.csv")
    print("- data/devices.csv")
    print()
    print(f"Services: {len(services_df)}")
    print(f"Devices: {len(devices_df)}")


if __name__ == "__main__":
    main()