const express = require('express');
const axios = require('axios');
const os = require('os');
const app = express();
const PORT = 3000;

// OPA on VM1
const OPA_URL = 'http://zt-vm1-control:8181/v1/data/httpauthz/allow';

app.use(express.json());

// Zero Trust Enforcement
async function enforceZeroTrust(req, res, next) {
  // Extract clean IPv4 address
  const sourceIp = req.ip.startsWith('::ffff:') ? req.ip.slice(7) : req.ip;

  const decision = {
    input: {
      method: req.method,
      headers: req.headers,
      source_ip: sourceIp
    }
  };

  console.log("DEBUG Source IP:", decision.input.source_ip);

  try {
    const { data } = await axios.post(OPA_URL, decision, { timeout: 5000 });

    // OPA returns simple { "result": true } or false
    if (data.result === true) {
      next();
    } else {
      res.status(403).json({ error: "Zero Trust: Access Denied" });
    }
  } catch (err) {
    console.error("OPA Error:", err.message);
    res.status(502).json({ error: "Policy Engine Down" });
  }
}

// Protected API
app.get('/api/data', enforceZeroTrust, (req, res) => {
  res.json({
    message: "Secure Data from VM2",
    server: "zt-vm2-app",
    timestamp: new Date().toISOString()
  });
});

// Get real external IP
const interfaces = os.networkInterfaces();
let ipAddress = '127.0.0.1';
Object.keys(interfaces).forEach((iface) => {
  interfaces[iface].forEach((details) => {
    if (details.family === 'IPv4' && !details.internal) {
      ipAddress = details.address;
    }
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`ZT App LIVE → http://${ipAddress}:${PORT}`);
});

