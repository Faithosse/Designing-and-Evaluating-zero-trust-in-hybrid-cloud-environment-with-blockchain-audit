# Test Procedures

## Overview

This document defines the functional and security test procedures for the Zero Trust prototype. The environment consists of:

- **VM1 – Control Plane**: Keycloak, OPA, Elasticsearch, Kibana, Filebeat, blockchain audit
- **VM2 – Application Plane**: NGINX Policy Enforcement Point (PEP)
- **VM3 – Network Security**: pfSense firewall and micro-segmentation gateway

Test objectives:

1. Verify **authentication** through Keycloak
2. Verify **authorization** through OPA and NGINX
3. Verify **tamper detection** through the blockchain audit chain
4. Measure **Mean Time To Detect (MTTD)** using the tampering detection workflow

These procedures align with the project evaluation methodology and environment. :contentReference[oaicite:2]{index=2}

---

## Test Environment

| VM | Role | IP Address | Services |
|---|---|---:|---|
| VM1 | Control Plane | 192.168.1.101 | Keycloak (8080), OPA (8181), Elasticsearch (9200), Kibana (5601), Filebeat, Blockchain audit |
| VM2 | Application Plane | 192.168.1.102 | NGINX PEP (3001) |
| VM3 | Network Security | 192.168.1.1/24 | pfSense firewall |

The Zero Trust network is segmented by pfSense, with VM1 and VM2 on the internal LAN segment and explicit allow rules only for required services. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

---

## Preconditions

Before running the test cases, confirm the platform is up.

### VM1 startup

```bash
docker start keycloak
docker start opa
docker start elasticsearch kibana
sudo systemctl start filebeat
curl -X PUT http://localhost:8181/v1/data/jwks \
  -H "Content-Type: application/json" \
  -d @/home/faith/zt-prototype/policies/jwks.json
docker ps
sudo systemctl status filebeat --no-pager | head -n 3
