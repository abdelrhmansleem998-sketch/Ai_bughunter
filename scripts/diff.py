import json
import sqlite3
import hashlib
import os

print("[*] Running Diff & SQLite State Management...")

db_path = "data/findings.db"
os.makedirs("data", exist_ok=True)

# الاتصال بقاعدة البيانات وإنشاء الجدول إذا لم يكن موجوداً
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS findings (
    hash TEXT PRIMARY KEY,
    host TEXT,
    name TEXT,
    severity TEXT,
    date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

new_findings = []

if os.path.exists("data/nuclei_output.json"):
    with open("data/nuclei_output.json", "r") as f:
        for line in f:
            try:
                finding = json.loads(line.strip())
                host = finding.get("host", "")
                name = finding.get("info", {}).get("name", "")
                severity = finding.get("info", {}).get("severity", "")
                
                # إنشاء البصمة الفريدة
                raw = f"{host}:{name}:{severity}"
                hash_val = hashlib.sha256(raw.encode()).hexdigest()
                
                # البحث في قاعدة البيانات
                cur.execute("SELECT hash FROM findings WHERE hash = ?", (hash_val,))
                if not cur.fetchone():
                    # ثغرة جديدة! إضافتها لقاعدة البيانات
                    cur.execute("INSERT INTO findings (hash, host, name, severity) VALUES (?, ?, ?, ?)", 
                                (hash_val, host, name, severity))
                    new_findings.append({
                        "host": host,
                        "name": name,
                        "severity": severity.upper(),
                        "url": finding.get("matched-at", host)
                    })
            except Exception as e:
                pass

conn.commit()
conn.close()

# حفظ الثغرات الجديدة في ملف منفصل ليقرأه الـ AI
with open("data/new_findings.json", "w") as f:
    json.dump(new_findings, f, indent=4)

print(f"[+] Found {len(new_findings)} NEW vulnerabilities.")
