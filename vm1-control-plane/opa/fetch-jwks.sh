#!/usr/bin/env bash
set -euo pipefail

KEYCLOAK_BASE="http://192.168.1.101:8080"
REALM="zt-realm"
OUT_DIR="$(pwd)/../policies"
OUT_FILE="$OUT_DIR/jwks.json"

mkdir -p "$OUT_DIR"

curl -s "${KEYCLOAK_BASE}/realms/${REALM}/protocol/openid-connect/certs" \
  | tee "$OUT_FILE" >/dev/null

echo "Saved JWKS to: $OUT_FILE"
