import os
import json
import requests

print("[*] Preparing Discord Report (v2)...")

webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
if not webhook_url: exit(1)

try:
    with open("data/new_findings.json", "r") as f:
        new_findings = json.load(f)
except FileNotFoundError:
    new_findings = []

if not new_findings: exit(0)

try:
    with open("reports/latest_report.md", "r") as f:
        ai_report = f.read()
except FileNotFoundError:
    ai_report = ""

if ai_report == "NO_NEW_FINDINGS": exit(0)

# اقتطاع التقرير لـ 1800 حرف كحد أقصى لتجنب قيود ديسكورد
safe_ai_report = ai_report[:1800] + ("..." if len(ai_report) > 1800 else "")

embed = {
    "title": "🚨 AI BugHunter: New Vulnerabilities!",
    "color": 16711680, 
    "description": f"**Found {len(new_findings)} New Vulnerability(ies)**\n\n**🤖 AI Analysis:**\n{safe_ai_report}", 
}

try:
    requests.post(webhook_url, json={"embeds": [embed]})
    print("[+] Discord alert sent!")
except Exception as e:
    print(f"[-] Discord error: {e}")
