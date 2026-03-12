# VM2 - Application Layer

## Purpose

VM2 hosts the protected application and acts as the **Policy Enforcement Point (PEP)** in the Zero Trust architecture.

The system uses **NGINX** to enforce authorization decisions by communicating with the **Open Policy Agent (OPA)** running on VM1.

This ensures that all application access requests are evaluated according to centralized policies.

## Services Hosted

| Service | Purpose | Port |
|------|------|------|
| NGINX | Reverse proxy and policy enforcement point | 3001 |
| Web application | Protected resource | 3001 |

## Directory Structure
vm2-application
├── nginx
├── scripts
└── web


### nginx

Contains the NGINX configuration used to protect application resources.

Example file:
protected.conf


This configuration forwards authorization checks to OPA on VM1.

### web

Contains the protected application content served by NGINX.

Example:
index.html


### scripts

Utility scripts for deployment and testing.

Examples:
deploy-nginx.sh
test-access.sh


## Authorization Flow

1. User authenticates with **Keycloak (VM1)**.
2. Keycloak issues a **JWT token**.
3. Client sends request to the protected application.
4. NGINX intercepts the request.
5. NGINX sends authorization check to **OPA on VM1**.
6. OPA evaluates policy.
7. Access is allowed or denied.

## Example Test

Attempt to access the protected resource:
curl http://VM2_IP:3001


If authorization is required, the request will be denied without a valid token.

## Notes

Before publishing the repository:

- remove environment-specific IP addresses
- replace credentials with placeholders
- avoid committing private tokens


