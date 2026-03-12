# VM1 - Zero Trust Control Plane

## Purpose

VM1 hosts the core Zero Trust control plane services.  
It provides identity management, policy evaluation, centralized logging, and tamper-evident auditing.

This machine acts as the **decision layer** of the architecture.

## Services Hosted

VM1 runs the following components:

| Service | Purpose | Port |
|------|------|------|
| Keycloak | Identity provider and JWT issuer | 8080 |
| Open Policy Agent (OPA) | Policy decision point | 8181 |
| Elasticsearch | Log indexing and storage | 9200 |
| Kibana | Log visualization | 5601 |
| Filebeat | Log shipping | — |
| Python audit chain | Tamper-evident audit logging | — |

## Directory Structure
vm1-control-plane
├── blockchain-audit
├── docker-compose.yml
├── opa
└── policies

### blockchain-audit
Contains the Python SHA-256 audit chain used to detect tampering with security events.

### docker-compose.yml
Defines the containerized services for:

- Keycloak
- Elasticsearch
- Kibana
- OPA

### opa
Configuration and runtime environment for Open Policy Agent.

### policies
Rego policies used by OPA to evaluate authorization decisions.

## Authentication Flow

1. User authenticates via **Keycloak**
2. Keycloak issues a **JWT token**
3. Client sends request to application (VM2)
4. NGINX forwards authorization check to **OPA**
5. OPA validates the token and evaluates policy
6. Access is **allowed or denied**

## Starting the Services

From the VM1 directory:
cd vm1-control-plane
docker compose up -d


Verify containers:
docker ps

## Accessing Services

Keycloak:
http://VM1_IP:8080


OPA API:
http://VM1_IP:8181

Elasticsearch:
http://VM1_IP:9200


Kibana:
http://VM1_IP:5601


## Policy Testing

Example policy query:
curl http://localhost:8181/v1/data/authz/allow


## Audit Integrity

The blockchain audit module creates a chain of hashed log entries.

Each record contains:

- timestamp
- event
- previous hash
- current hash

If a record is modified, the chain verification will fail.

