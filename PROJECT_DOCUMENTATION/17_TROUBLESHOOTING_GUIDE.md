# 17. Troubleshooting Guide

This guide details common issues, system faults, and resolution steps when running the Aditya-L1 Space Weather Intelligence Platform.

---

## 🔌 Issue 1: Port Conflict (Address Already In Use)

### Symptoms
When starting the FastAPI backend with Uvicorn, you receive the error:
`[Errno 48] Address already in use` or receive 404s/403s on `http://localhost:8000`.

### Root Cause
An orphaned Python process from a previous run or another project (e.g. Taskswarm) is holding onto port 8000.

### Resolution
Identify the PID holding the port and terminate it:
```bash
# Locate PID
lsof -i :8000

# Terminate process
kill -9 <PID>
```
Restart the Uvicorn backend.

---

## 📡 Issue 2: WebSocket Connection Drops or Fails to Connect

### Symptoms
The frontend dashboard displays a persistent "Reconnecting..." state, and telemetry charts do not update.

### Troubleshooting Steps
1.  **Check Backend Server**: Verify the Uvicorn log is active and not showing traceback errors.
2.  **Verify Port Configuration**: Open your browser's inspect console and check if the client is trying to connect to the correct port (e.g. `ws://localhost:8000/ws/live` vs `ws://localhost:5174/ws/live`).
3.  **CORS & Origin Checks**: If deployed behind a reverse proxy, ensure Nginx headers allow connection upgrading:
    ```nginx
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    ```

---

## 🌡️ Issue 3: Missing Digital Twin Packets in WebSocket stream

### Symptoms
The streaming test runner or frontend warns about missing `digital_twin` updates.

### Root Cause
The `_generate_digital_twin` loop in `backend/events/generator.py` publishes updates at a lower frequency (5 seconds) than the telemetry channel (1 second). If a script exits too quickly (e.g. after receiving only 10-20 packets), it will miss the digital twin packets.

### Resolution
*   Ensure verification scripts wait at least **5–10 seconds** or read up to **40 packets** before validating channel completeness.
*   Check if the background loops in `generator.py` are started properly at app startup.
