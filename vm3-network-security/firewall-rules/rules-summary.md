# pfSense Firewall Rules Summary

## Purpose

VM3 runs pfSense and provides the network segmentation and firewall enforcement layer for the Zero Trust architecture.

## Interfaces

- WAN: 10.0.2.15/24
- LAN: 192.168.1.1/24

## Internal Hosts

- VM1 Control Plane: 192.168.1.101
- VM2 Application: 192.168.1.102
- VM3 pfSense: 192.168.1.1

## Security Posture

Default deny was applied. Only explicitly required traffic was allowed.

## Allowed Traffic

| Source | Destination | Port | Purpose |
|------|------|------|------|
| VM2 | VM1 | 8181 | OPA policy checks |
| VM2 | VM1 | 8080 | Keycloak access |
| VM1 | VM1 | 9200 | Elasticsearch |
| VM1 | VM1 | 5601 | Kibana |
| Client | VM2 | 3001 | Protected application access |

## Zero Trust Role

pfSense enforces network-level least privilege and limits lateral movement between virtual machines.
