# Data Dictionary

This file defines the final schema for the synthetic telecom service assurance dataset.

---

## 1) incidents.csv

| Column | Type | Example | Description |
|---|---|---|---|
| incident_id | string | INC0001 | Unique incident identifier |
| incident_start_time | datetime | 2026-03-01 10:05:00 | Incident start time |
| incident_end_time | datetime | 2026-03-01 10:42:00 | Incident end time |
| region | string | Toronto | Geographic region |
| site_id | string | SITE014 | Main impacted site |
| service_id | string | SVC003 | Main impacted service |
| root_cause | string | fiber_cut | Simulated root cause label |
| priority | string | critical | Incident urgency level |
| customer_impact_count | integer | 1240 | Estimated number of customers affected |
| site_impact_count | integer | 6 | Estimated number of impacted sites |
| ticket_status | string | resolved | Current incident ticket status |

---

## 2) alarms.csv

| Column | Type | Example | Description |
|---|---|---|---|
| alarm_id | string | ALM000001 | Unique alarm identifier |
| incident_id | string | INC0001 | Incident this alarm belongs to |
| timestamp | datetime | 2026-03-01 10:05:12 | Alarm event time |
| device_id | string | DEV0021 | Device generating the alarm |
| alarm_type | string | link_down | Alarm category |
| severity | string | critical | Alarm severity |
| alarm_text | string | Link down detected on aggregation uplink | Human-readable alarm description |
| vendor | string | Cisco | Device vendor |
| technology | string | IP_MPLS | Network technology |
| acknowledged | boolean | True | Whether NOC acknowledged the alarm |
| cleared | boolean | False | Whether alarm has cleared |

---

## 3) devices.csv

| Column | Type | Example | Description |
|---|---|---|---|
| device_id | string | DEV0021 | Unique device identifier |
| device_name | string | TOR-RTR-21 | Human-readable device name |
| device_type | string | router | Device category |
| vendor | string | Cisco | Device vendor |
| technology | string | IP_MPLS | Technology domain |
| region | string | Toronto | Device region |
| site_id | string | SITE014 | Site where device is located |
| service_id | string | SVC003 | Main linked service |

---

## 4) services.csv

| Column | Type | Example | Description |
|---|---|---|---|
| service_id | string | SVC003 | Unique service identifier |
| service_name | string | Toronto Mobile Data Cluster | Human-readable service name |
| service_type | string | Mobile Data | Service category |
| customer_segment | string | Consumer | Customer segment |
| sla_tier | string | Gold | Service SLA tier |

---

## Controlled Values

### Regions
- Toronto
- Mississauga
- Ottawa
- Brampton

### Device types
- router
- switch
- base_station
- core_node
- gateway
- fiber_hub

### Vendors
- Ericsson
- Nokia
- Huawei
- Cisco
- Juniper

### Technologies
- 4G
- 5G
- IP_MPLS
- Fiber
- Microwave

### Service types
- Mobile Data
- Voice
- SMS
- Broadband
- Enterprise VPN

### Customer segments
- Consumer
- Business
- Enterprise

### SLA tiers
- Bronze
- Silver
- Gold
- Platinum

### Root causes
- fiber_cut
- power_failure
- router_failure
- configuration_error
- congestion
- software_bug

### Priorities
- low
- medium
- high
- critical

### Alarm types
- link_down
- packet_loss
- latency_high
- utilization_high
- device_unreachable
- power_alarm
- config_mismatch
- service_degraded
- cpu_high
- memory_high

### Severities
- minor
- major
- critical

### Ticket status
- open
- in_progress
- resolved