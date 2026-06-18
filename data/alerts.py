# Standalone reference file — shows intended data structure.
# In production, this data lives in PostgreSQL and is queried via app.py.

alerts = [
    {
        "id": 1,
        "alert": "Ransomware signature detected",
        "severity": "critical",
        "source_ip": "192.168.1.55",
        "status": "investigating",
        "timestamp": "2026-06-17 08:14:02",
    },
    {
        "id": 2,
        "alert": "Unusual data exfiltration",
        "severity": "critical",
        "source_ip": "10.0.0.99",
        "status": "open",
        "timestamp": "2026-06-17 09:02:17",
    },
    {
        "id": 3,
        "alert": "Phishing email detected",
        "severity": "high",
        "source_ip": "172.16.0.12",
        "status": "contained",
        "timestamp": "2026-06-17 07:47:33",
    },
    {
        "id": 4,
        "alert": "Brute force login attempt",
        "severity": "high",
        "source_ip": "185.220.101.47",
        "status": "investigating",
        "timestamp": "2026-06-17 10:30:05",
    },
    {
        "id": 5,
        "alert": "DDoS traffic spike",
        "severity": "medium",
        "source_ip": "203.0.113.9",
        "status": "open",
        "timestamp": "2026-06-17 11:55:44",
    },
    {
        "id": 6,
        "alert": "Malware signature detected",
        "severity": "critical",
        "source_ip": "192.168.2.14",
        "status": "open",
        "timestamp": "2026-06-17 06:22:11",
    },
    {
        "id": 7,
        "alert": "Unauthorized access attempt",
        "severity": "medium",
        "source_ip": "10.0.1.99",
        "status": "resolved",
        "timestamp": "2026-06-17 05:10:58",
    },
    {
        "id": 8,
        "alert": "Phishing email detected",
        "severity": "low",
        "source_ip": "192.168.1.200",
        "status": "resolved",
        "timestamp": "2026-06-17 04:05:30",
    },
]