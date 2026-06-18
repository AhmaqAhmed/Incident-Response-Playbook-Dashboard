import json
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

# ── Database connection ──────────────────────────────────────────────────────
# Replace these credentials with your own before running
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "ir_dashboard",
    "user":     "postgres",
    "password": "root",
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# ── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    severity_filter = request.args.get("severity", "all")

    conn = get_conn()
    cur = conn.cursor()

    # Fetch alerts (filtered or all)
    if severity_filter != "all":
        cur.execute(
            """
            SELECT id, alert, severity, source_ip, status,
                   TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp
            FROM alerts
            WHERE severity = %s
            ORDER BY timestamp DESC
            """,
            (severity_filter,),
        )
    else:
        cur.execute(
            """
            SELECT id, alert, severity, source_ip, status,
                   TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp
            FROM alerts
            ORDER BY timestamp DESC
            """
        )

    rows = cur.fetchall()
    alerts = [
        {
            "id":        r[0],
            "alert":     r[1],
            "severity":  r[2],
            "source_ip": r[3],
            "status":    r[4],
            "timestamp": r[5],
        }
        for r in rows
    ]

    # Summary counts always from full table (not filtered)
    cur.execute("SELECT COUNT(*) FROM alerts")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'critical'")
    critical = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM alerts WHERE status = 'open'")
    open_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM alerts WHERE status = 'resolved'")
    resolved = cur.fetchone()[0]

    cur.close()
    conn.close()

    summary = {
        "total":    total,
        "critical": critical,
        "open":     open_count,
        "resolved": resolved,
    }

    return render_template(
        "preview.html",
        alerts_json=json.dumps(alerts),
        summary=summary,
        severity_filter=severity_filter,
    )


if __name__ == "__main__":
    app.run(debug=True)