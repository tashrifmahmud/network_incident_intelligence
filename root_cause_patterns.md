# Root Cause Patterns

This file defines the typical alarm behavior, impact level, and troubleshooting direction for each simulated telecom root cause.

---

## 1) fiber_cut

### Typical behavior
- Usually affects multiple devices in the same area
- Often causes sudden service degradation across a region or site cluster
- Usually high customer impact
- Common in Fiber or IP_MPLS environments

### Common alarm types
- link_down
- device_unreachable
- service_degraded
- packet_loss

### Common device types
- fiber_hub
- router
- gateway
- switch

### Common severity mix
- critical
- major

### Typical priority
- critical

### Typical customer impact
- high

### Suggested troubleshooting
- Check physical fiber path
- Verify optical link state
- Check if multiple nearby devices lost connectivity
- Escalate for field investigation if needed

---

## 2) power_failure

### Typical behavior
- Often impacts one site heavily
- Devices at the same site may go unreachable together
- Can affect radio/base station environments strongly
- Usually sudden and severe

### Common alarm types
- power_alarm
- device_unreachable
- service_degraded
- link_down

### Common device types
- base_station
- gateway
- router
- core_node

### Common severity mix
- critical
- major

### Typical priority
- critical

### Typical customer impact
- medium to high

### Suggested troubleshooting
- Verify commercial power status
- Check site power systems and backup battery
- Confirm whether all devices at site are affected
- Escalate site power issue

---

## 3) router_failure

### Typical behavior
- Usually centered on one important device
- Can create downstream connectivity issues
- Device may become unreachable or unstable
- Often impacts multiple connected services

### Common alarm types
- device_unreachable
- link_down
- cpu_high
- memory_high

### Common device types
- router
- core_node
- gateway

### Common severity mix
- critical
- major

### Typical priority
- high to critical

### Typical customer impact
- medium to high

### Suggested troubleshooting
- Check device reachability
- Verify hardware health
- Review CPU and memory spikes
- Reroute traffic if possible
- Escalate hardware replacement if persistent

---

## 4) configuration_error

### Typical behavior
- Often happens after a change or deployment
- Can affect one service more than one whole region
- Devices may stay online but service quality drops
- Usually not a total outage at first

### Common alarm types
- config_mismatch
- service_degraded
- latency_high
- packet_loss

### Common device types
- router
- switch
- gateway
- core_node

### Common severity mix
- major
- minor

### Typical priority
- medium to high

### Typical customer impact
- low to medium

### Suggested troubleshooting
- Review recent configuration changes
- Compare intended and actual config state
- Roll back recent changes if needed
- Validate affected service path

---

## 5) congestion

### Typical behavior
- Usually appears during heavy usage periods
- Service remains available but quality drops
- Often seen as latency and packet loss
- More likely in mobile data or broadband services

### Common alarm types
- latency_high
- packet_loss
- utilization_high
- cpu_high

### Common device types
- base_station
- router
- gateway
- switch

### Common severity mix
- major
- minor

### Typical priority
- medium to high

### Typical customer impact
- medium

### Suggested troubleshooting
- Check traffic utilization
- Identify peak usage patterns
- Review capacity thresholds
- Consider load balancing or capacity expansion

---

## 6) software_bug

### Typical behavior
- Device remains partially functional
- Performance degrades or unstable behavior appears
- Symptoms may overlap with congestion or hardware issues
- Usually needs correlation across repeated patterns

### Common alarm types
- service_degraded
- cpu_high
- memory_high
- packet_loss
- latency_high

### Common device types
- core_node
- gateway
- router
- base_station

### Common severity mix
- major
- minor

### Typical priority
- medium to high

### Typical customer impact
- low to medium

### Suggested troubleshooting
- Review recent software release or patch history
- Compare recurring incidents across similar devices
- Check memory/CPU trend behavior
- Escalate to software engineering if repeatable