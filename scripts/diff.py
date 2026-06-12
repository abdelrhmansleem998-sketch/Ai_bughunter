import json
import sqlite3
import hashlib
import os
from datetime import datetime

print("[*] Running State Management (v2)...")

db_path = "data/findings.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS findings (
    hash TEXT PRIMARY KEY,
    host TEXT,
    name TEXT,
    severity TEXT,
    template_id TEXT,
    matched_at TEXT,
    first_seen TIMESTAMP
)
""")

new_findings = []

if os.path.exists("data/nuclei_output.json"):
    with open("data/nuclei_output.json", "r") as f:
        for line in f:
            if not line.strip(): continue
            try:
                finding = json.loads(line.strip())
                host = finding.get("host", "unknown")
                name = finding.get("info", {}).get("name", "unknown")
                severity = finding.get("info", {}).get("severity", "info")
                template_id = finding.get("template-id", "unknown")
                matched_at = finding.get("matched-at", host)
                
                # البصمة الاحترافية (لا تتداخل فيها الثغرات)
                raw = f"{host}:{template_id}:{severity}:{matched_at}"
                hash_val = hashlib.sha256(raw.encode()).hexdigest()
                
                cur.execute("SELECT hash FROM findings WHERE hash = ?", (hash_val,))
                if not cur.fetchone():
                    now = datetime.now().isoformat()
                    cur.execute("INSERT INTO findings VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                (hash_val, host, name, severity, template_id, matched_at, now))
                    
                    new_findings.append({
                        "host": host, "name": name, "severity": severity.upper(),
                        "url": matched_at, "template": template_id
                    })
            except Exception:
                pass

conn.commit()
conn.close()

with open("data/new_findings.json", "w") as f:
    json.dump(new_findings, f, indent=4)

print(f"[+] Found {len(new_findings)} NEW vulnerabilities.")
