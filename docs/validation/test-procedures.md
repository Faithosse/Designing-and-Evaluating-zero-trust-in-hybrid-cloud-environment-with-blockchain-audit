# Zero Trust System Test Procedures

## Overview

This document describes the testing procedures used to validate the Zero Trust architecture implemented in this project.

The prototype environment consists of three virtual machines.

| VM | Role | Components |
|---|---|---|
| VM1 | Control Plane | Keycloak, Open Policy Agent (OPA), Elasticsearch, Kibana, Filebeat, Blockchain Audit |
| VM2 | Application Layer | NGINX Policy Enforcement Point |
| VM3 | Network Security | pfSense firewall and micro-segmentation |

The testing procedures verify the following security properties:

1. Authentication
2. Authorization
3. Tamper Detection
4. Mean Time To Detect (MTTD)
5. Centralized Logging

---

# 1 Authentication Test

## Objective

Verify that the Keycloak Identity Provider successfully authenticates users and issues a valid JSON Web Token (JWT).

Keycloak serves as the Identity Provider within the Zero Trust architecture and signs JWT tokens using RSA-SHA256 after validating user credentials.

## Environment

VM1 – Control Plane

Service: Keycloak

Address

```
http://192.168.1.101:8080
```

Realm

```
zt-realm
```

Client

```
zt-client
```

Test user

```
username: paul_faith
password: AdminPass2025!
```

## Procedure

Execute the following command from a terminal:

```
curl -X POST http://192.168.1.101:8080/realms/zt-realm/protocol/openid-connect/token \
-d "client_id=zt-client" \
-d "username=paul_faith" \
-d "password=AdminPass2025!" \
-d "grant_type=password"
```

## Expected Result

The server returns a JSON response containing a JWT access token.

Example output

```
{
 "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Validation

The token payload can be inspected with:

```
echo "$TOKEN" | cut -d "." -f2 | base64 -d | jq
```

Expected JWT claims include

```
iss
sub
aud
exp
iat
```

## Evidence

Screenshots should be stored in

```
docs/screenshots/authentication/
```

Example filename

```
keycloak-token.png
```

---

# 2 Authorization Test

## Objective

Verify that Open Policy Agent evaluates authorization policies and that NGINX enforces the authorization decision.

OPA acts as the Policy Decision Point (PDP) while NGINX acts as the Policy Enforcement Point (PEP).

The policy evaluates

- JWT validity
- token issuer
- token audience
- source IP address

---

## Test 2.1 Valid Token Access

### Procedure

Acquire a token using the authentication procedure.

Then test the authorization policy.

```
curl -X POST http://localhost:8181/v1/data/httpauthz/allow \
-H "Content-Type: application/json" \
-d '{"input":{"method":"GET","headers":{"Authorization":"Bearer '$TOKEN'"},"source_ip":"192.168.1.102"}}'
```

Then test the protected application endpoint.

```
curl -H "Authorization: Bearer $TOKEN" http://192.168.1.102:3001/
```

### Expected Result

OPA response

```
true
```

NGINX response

```
HTTP 200 OK
```

The protected application content should be returned.

---

## Test 2.2 No Token

### Procedure

Attempt to access the application without authentication.

```
curl http://192.168.1.102:3001/
```

### Expected Result

```
403 Forbidden
```

---

## Test 2.3 Invalid IP Address

### Procedure

Send an authorization request with an unauthorized source IP.

```
curl -X POST http://localhost:8181/v1/data/httpauthz/allow \
-H "Content-Type: application/json" \
-d '{"input":{"method":"GET","headers":{"Authorization":"Bearer '$TOKEN'"},"source_ip":"10.10.10.10"}}'
```

### Expected Result

OPA response

```
false
```

---

## Evidence

Screenshots stored in

```
docs/screenshots/authorization/
```

Example files

```
opa-allow.png
opa-deny.png
nginx-403.png
```

---

# 3 Tamper Detection Test

## Objective

Verify that the blockchain based audit system detects tampering with logged events.

The blockchain audit mechanism stores security events using SHA-256 hash chaining. Any modification of stored records breaks the chain and is immediately detectable.

---

## Procedure

Navigate to the blockchain audit directory.

```
cd ~/zt-prototype/blockchain-audit
```

Add new audit blocks.

```
./audit_chain.py add '{"type":"OPA_DECISION","result":true,"user":"paul_faith"}'
./audit_chain.py add '{"type":"OPA_DECISION","result":false,"user":"unknown"}'
```

Verify the blockchain.

```
./audit_chain.py verify
```

### Expected Result

```
Blockchain verified successfully
```

---

## Tampering Simulation

Modify an existing block in the blockchain file.

```
nano audit_chain.json
```

Change a stored value such as

```
result:true → result:false
```

Run verification again.

```
./audit_chain.py verify
```

### Expected Result

Verification fails and reports a hash mismatch.

---

## Evidence

Screenshots stored in

```
docs/screenshots/tamper-detection/
```

Example

```
audit-chain-clean.png
audit-chain-tampered.png
```

---

# 4 Mean Time To Detect (MTTD)

## Objective

Measure how quickly the blockchain audit mechanism detects tampering.

Mean Time To Detect represents the time between tampering with the audit log and the detection of that tampering.

---

## Procedure

Execute the detection test script.

```
~/mttd_test.sh
```

### Expected Result

The script reports detection latency.

Example output

```
Tamper detected in 88.171 ms
```

This demonstrates sub-second detection of insider attacks.

---

## Evidence

Screenshots stored in

```
docs/screenshots/mttd/
```

Example

```
mttd-result.png
```

---

# 5 Logging Verification Test

## Objective

Verify that logs are successfully collected and visualized using the ELK stack.

---

## Procedure

Open Kibana in a browser.

```
http://192.168.1.101:5601
```

Navigate to

```
Analytics → Discover
```

Select index

```
filebeat-*
```

---

## Expected Result

Log entries appear showing authorization events from OPA and the application layer.

These logs confirm that Filebeat successfully ships logs to Elasticsearch and Kibana visualizes them in real time.

---

## Evidence

Screenshots stored in

```
docs/screenshots/logging/
```

Example

```
kibana-logs.png
```

---

# Summary of Expected Results

| Test | Expected Result |
|-----|----------------|
| Authentication | Keycloak issues valid JWT token |
| Authorization (valid token) | OPA returns true and NGINX returns HTTP 200 |
| Authorization (no token) | NGINX returns 403 |
| Authorization (invalid IP) | OPA returns false |
| Tamper Detection | Blockchain verification fails after modification |
| Chain Restoration | Blockchain verifies successfully again |
| MTTD Test | Tampering detected in milliseconds |
| Logging Test | Security events visible in Kibana |

---

# Screenshot Folder Structure

. 
