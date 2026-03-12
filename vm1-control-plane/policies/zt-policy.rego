package httpauthz
import future.keywords.if

default allow := false

# ---- Config ----
allowed_cidrs := {"192.168.1.0/24", "192.168.0.0/24"}
required_issuer := "http://192.168.1.101:8080/realms/zt-realm"
allowed_audiences := {"zt-client", "account"}

# ---- Helpers ----
bearer_token := t if {
    h := input.headers["Authorization"]
    startswith(h, "Bearer ")
    t := substring(h, count("Bearer "), -1)
}

src_allowed if {
    cidr := allowed_cidrs[_]
    net.cidr_contains(cidr, input.source_ip)
}

claims := c if {
    tok := bearer_token
    [_, c, _] := io.jwt.decode(tok)
}

issuer_ok if {
    claims.iss == required_issuer
}

aud_ok if {
    claims.aud in allowed_audiences
}

# JWT validation: checks token is well-formed (io.jwt.decode would fail on garbage)
# Note: In production, add io.jwt.verify_rs256() for cryptographic verification
valid_jwt if {
    bearer_token != ""
    count(claims) > 0
}

# ---- Decision ----
allow if {
    input.method == "GET"
    src_allowed
    valid_jwt
    issuer_ok
    aud_ok
}
