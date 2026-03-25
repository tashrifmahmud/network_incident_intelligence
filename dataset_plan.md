# Dataset Plan

## Goal
Build a synthetic but realistic telecom service assurance dataset for AI experiments in:
- root cause classification
- incident clustering
- troubleshooting recommendation
- priority scoring

## Files
- incidents.csv
- alarms.csv
- devices.csv
- services.csv

---

## 1) incidents.csv
One row = one network incident

### Columns
- incident_id
- incident_start_time
- incident_end_time
- region
- site_id
- service_id
- root_cause
- priority
- customer_impact_count
- site_impact_count
- ticket_status

### Description
This is the master incident table. It represents a service-impacting event that may contain multiple alarms across one or more devices.

---

## 2) alarms.csv
One row = one alarm/event tied to an incident

### Columns
- alarm_id
- incident_id
- timestamp
- device_id
- alarm_type
- severity
- alarm_text
- vendor
- technology
- acknowledged
- cleared

### Description
This is the raw event stream. Multiple alarms can belong to the same incident.

---

## 3) devices.csv
One row = one network device

### Columns
- device_id
- device_name
- device_type
- vendor
- technology
- region
- site_id
- service_id

### Description
This is the device inventory table. It connects alarms to actual network infrastructure.

---

## 4) services.csv
One row = one customer-facing service

### Columns
- service_id
- service_name
- service_type
- customer_segment
- sla_tier

### Description
This connects technical events to business/customer impact, which is important in service assurance.

---

## Category Values

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