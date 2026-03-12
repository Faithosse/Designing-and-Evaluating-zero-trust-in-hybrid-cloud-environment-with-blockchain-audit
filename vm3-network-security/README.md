# VM3 - Network Security Layer

## Purpose

VM3 runs **pfSense** and provides the network security boundary for the Zero Trust architecture.

It acts as:

- the **default gateway**
- the **internal firewall**
- the **micro-segmentation controller**

All traffic between the internal virtual machines passes through pfSense, ensuring that access is explicitly controlled.

## Network Configuration

| Interface | Address | Purpose |
|------|------|------|
| WAN | 10.0.2.15/24 | External network access |
| LAN | 192.168.1.1/24 | Internal Zero Trust network |

The internal virtual machines are connected to the LAN network.

Example addressing:

| Machine | IP |
|------|------|
| VM1 Control Plane | 192.168.1.101 |
| VM2 Application | 192.168.1.102 |
| VM3 pfSense | 192.168.1.1 |

## Firewall Policy

pfSense enforces a **default deny** rule.

Only explicitly required services are permitted.

### Allowed Traffic

| Source | Destination | Port | Purpose |
|------|------|------|------|
| VM2 | VM1 | 8181 | OPA authorization checks |
| VM2 | VM1 | 8080 | Keycloak authentication |
| VM1 | VM1 | 9200 | Elasticsearch |
| VM1 | VM1 | 5601 | Kibana |
| Client | VM2 | 3001 | Application access |

All other traffic is blocked.

## Micro-Segmentation

The firewall ensures that:

- application servers cannot directly access identity infrastructure unless required
- lateral movement between machines is limited
- unauthorized network requests are blocked

This enforces the **Zero Trust principle of least privilege networking**.

## pfSense Management

The pfSense administration interface can be accessed through:

https://VM3_IP
vm3-network-security/ping_vm1_vm2.png

Default management port:
443


## Validation

To verify connectivity between the machines:

From VM2:
ping 192.168.1.101


Test OPA connectivity:
curl http://192.168.1.101:8181


## Documentation

Screenshots and firewall rule exports are stored in:
vm3-network-security/screenshots
vm3-network-security/firewall-rules


