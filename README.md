# Desinging and Evaluating Zero Trust in Hybrid Cloud with Blockchain-Backed Audit Trail

## Overview

This project implements a Zero Trust security prototype in a hybrid-style virtualised environment using three virtual machines. The design combines identity-based access control, policy-based authorization, network micro-segmentation, centralized observability, and tamper-evident audit logging.

The system is built around three roles:

- **VM3**: pfSense firewall and micro-segmentation gateway
- **VM1**: control plane for identity, policy, logging, and audit integrity
- **VM2**: protected application layer using NGINX as a Policy Enforcement Point (PEP)

The architecture follows the Zero Trust principle of **never trust, always verify**, ensuring that access is continuously validated at the network, identity, and application layers.

## Objectives

The project aims to:

- enforce Zero Trust access control across segmented virtual machines
- validate JWT-based authentication and authorization
- implement network micro-segmentation using pfSense
- centralize security telemetry using the Elastic Stack
- maintain tamper-evident audit records using a SHA-256 blockchain-style log chain
- demonstrate a lightweight and reproducible research prototype

## Architecture Summary

The environment consists of three interconnected virtual machines:

### VM3 — Network Security and Micro-Segmentation
VM3 runs pfSense and acts as the default gateway, security boundary, and internal segmentation layer.

- **WAN:** `10.0.2.15/24`
- **LAN:** `192.168.1.1/24`

VM3 enforces a default-deny posture and only permits explicitly required services.

### VM1 — Control Plane
VM1 hosts the core Zero Trust decision and observability services.

- Keycloak — identity provider and JWT issuer
- Open Policy Agent (OPA) — policy decision point
- Elasticsearch — centralized indexing and log storage
- Kibana — monitoring and visualization
- Filebeat — log forwarding
- Python SHA-256 audit chain — tamper-evident audit trail

### VM2 — Application Layer
VM2 hosts the protected application and acts as the enforcement point.

- NGINX — Policy Enforcement Point (PEP)
- protected application content
- request forwarding for policy validation to OPA on VM1

## Deployment Order

The system should be deployed in this order:

1. **VM3 (pfSense)**
2. **VM1 (Control Plane)**
3. **VM2 (Application Layer)**

This order is required because network segmentation must be established before services can communicate securely.

## Repository Structure

```text
.
├── README.md
├── docs/
│   ├── architecture/
│   ├── screenshots/
│   └── validation/
├── vm1-control-plane/
│   ├── README.md
│   ├── blockchain-audit/
│   ├── docker-compose.yml
│   ├── opa/
│   └── policies/
├── vm2-application/
│   ├── README.md
│   ├── nginx/
│   ├── scripts/
│   └── web/
└── vm3-network-security/
    ├── README.md
    ├── firewall-rules/
    └── screenshots/



Technology Stack

Keycloak 22 — OpenID Connect identity and JWT issuance

Open Policy Agent (OPA) — authorization and policy evaluation

pfSense — network micro-segmentation and firewall enforcement

Elastic Stack 8.11 — logging, analytics, and visualization

Filebeat — lightweight log shipping

Python with SHA-256 hashing — tamper-evident local audit chain

NGINX — application-layer Policy Enforcement Point

Zero Trust Flow

A typical access flow is:

A user authenticates through Keycloak on VM1

Keycloak issues a signed JWT

The user attempts to access the protected application on VM2

NGINX forwards the authorization check to OPA on VM1

OPA evaluates policy based on token validity, claims, and request context

The decision is enforced by NGINX

Logs are forwarded into the Elastic Stack

Security-relevant events are recorded in the blockchain-backed audit trail

Firewall Policy Overview

The pfSense layer is configured with explicit allow rules for required services only:

Keycloak — TCP 8080

OPA — TCP 8181

Elasticsearch — TCP 9200

Kibana — TCP 5601

NGINX application access — TCP 3001

All other traffic is denied by default.

Reproducibility Notes

This repository is intended to support technical reproducibility of the prototype. It includes implementation artifacts, configuration structure, scripts, and documentation for each VM role.


Current Status

This repository is being assembled from the working VM-based implementation. The technical structure reflects the deployed system across the three virtual machines.

Author

Faith
