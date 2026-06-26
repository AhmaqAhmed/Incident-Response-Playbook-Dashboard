# Incident Response Playbook Dashboard

A Flask web application that simulates a Security Operations Center (SOC) analyst workflow — security alerts are detected, triaged by severity, and resolved by following structured incident response playbooks. Alert data is stored in PostgreSQL and served dynamically to the dashboard.

---

## Project Structure

```
ir-dashboard/
├── app.py                  # Flask routes and PostgreSQL integration
├── data/
│   ├── alerts.py           # Reference: intended alert data structure
│   └── playbooks.py        # Reference: intended playbook structure
├── templates/
│   └── preview.html        # Single-file Jinja2 template (dashboard + detail page)
├── screenshots/            # Splunk SIEM evidence screenshots
└── README.md
```

---

## Features

- **Alert dashboard** — displays all incidents in a table, color-coded by severity (critical / high / medium / low)
- **Metric cards** — live counts for total alerts, critical alerts, open incidents, and resolved incidents
- **Severity filter** — filter the alert table by severity via a dropdown
- **Playbook step-through** — clicking any alert opens a detail page with structured response steps
- **Evidence notes** — free-text field on the detail page for analyst observations
- **PostgreSQL backend** — all alert data stored and queried from a relational database

---

## SIEM Integration

Splunk Enterprise Search & Reporting was used to identify real Windows Security events that informed the alert data in this dashboard.

**Splunk SPL queries used:**

```spl
-- All events in winlog index (September 2022)
index="winlog_clients"

-- Failed logon attempts for admin accounts (EventCode 4625)
source="WinEventLog:*" index="winlog_clients" EventCode=4625 AND Nom_du_compte=Admin*
```

**Events detected and logged:**

| Splunk EventCode | Description | Mapped Alert |
|---|---|---|
| 4625 | Failed logon attempt | Brute Force Login Attempt |
| 4624 | Successful logon | Unauthorized Access Attempt |
| 4634 | Account logoff | Unauthorized Access Attempt |
| 4672 | Special privileges assigned | Unauthorized Access Attempt |

Screenshots of Splunk searches and saved reports are available in the `/screenshots` folder.

---

## Alert Types & Playbooks

| Alert | Severity | Playbook Steps |
|---|---|---|
| Ransomware signature detected | Critical | Isolate → Forensics → Notify → Restore |
| Unusual data exfiltration | Critical | Identify user → Block → Audit → Notify legal |
| Phishing email detected | High | Block sender → Reset creds → Scan endpoints |
| Brute Force Login Attempt | High | Lock account → Block IP → Enable MFA |
| DDoS traffic spike | Medium | Rate limit → ISP scrubbing → Monitor |
| Malware signature detected | Critical | Isolate → AV scan → Forensics → Restore |
| Unauthorized Access Attempt | Medium | Review logs → Verify → Harden access |

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ir-dashboard.git
cd ir-dashboard
```

### 2. Install dependencies
```bash
pip install flask psycopg2
```

### 3. Create the database
```sql
CREATE DATABASE ir_dashboard;
\c ir_dashboard

CREATE TABLE alerts (
    id        SERIAL PRIMARY KEY,
    alert     VARCHAR(100),
    severity  VARCHAR(20),
    source_ip VARCHAR(45),
    status    VARCHAR(20),
    timestamp TIMESTAMP
);
```

### 4. Seed alert data
```sql
-- Splunk-sourced events (Windows Security logs)
INSERT INTO alerts (alert, severity, source_ip, status, timestamp) VALUES
('Brute Force Login Attempt',   'high',   '192.168.1.88', 'investigating', '2022-09-02 06:21:10'),
('Brute Force Login Attempt',   'high',   '192.168.1.88', 'resolved',      '2022-09-02 06:24:26'),
('Unauthorized Access Attempt', 'medium', '192.168.1.88', 'resolved',      '2022-09-02 10:17:40');

-- Simulated alerts covering remaining incident types
INSERT INTO alerts (alert, severity, source_ip, status, timestamp) VALUES
('Ransomware signature detected', 'critical', '192.168.1.55', 'investigating', '2026-06-17 08:14:02'),
('Unusual data exfiltration',     'critical', '10.0.0.99',    'open',          '2026-06-17 09:02:17'),
('Phishing email detected',       'high',     '172.16.0.12',  'contained',     '2026-06-17 07:47:33'),
('DDoS traffic spike',            'medium',   '203.0.113.9',  'open',          '2026-06-17 11:55:44'),
('Malware signature detected',    'critical', '192.168.2.14', 'open',          '2026-06-17 06:22:11');
```

### 5. Configure database credentials
In `app.py`, update `DB_CONFIG`:
```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "ir_dashboard",
    "user":     "postgres",
    "password": "your_password_here",
}
```

### 6. Run the app
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Skills Demonstrated

- Flask routing and Jinja2 templating
- PostgreSQL database design and querying with psycopg2
- Incident triage and severity classification
- Playbook-driven incident response
- SIEM tooling awareness (Splunk Search & Reporting, SPL queries)
- Security dashboard development

---

## Blog Post

A full writeup of the project journey — initial design decisions, Jinja2 struggles, moving from dummy data to a live database, and integrating Splunk — is available here:

[Building an Incident Response Playbook Dashboard](https://first-projects-blog.hashnode.dev/building-an-incident-response-playbook-dashboard)

---

## Screenshots

Splunk SIEM evidence and dashboard screenshots are available in the `/screenshots` folder.
