import os
import json
import requests

print("[*] Preparing Discord Report...")

webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
if not webhook_url:
    print("[-] DISCORD_WEBHOOK_URL not found in secrets.")
    exit(1)

try:
    with open("data/new_findings.json", "r") as f:
        new_findings = json.load(f)
except FileNotFoundError:
    new_findings = []

if not new_findings:
    print("[*] No new findings to report today.")
    exit(0)

# قراءة تحليل الذكاء الاصطناعي
try:
    with open("reports/latest_report.md", "r") as f:
        ai_report = f.read()
except FileNotFoundError:
    ai_report = "AI Report missing."

# بناء رسالة الديسكورد (Embed)
embed = {
    "title": "🚨 BugHunter AI: New Vulnerabilities Detected!",
    "color": 16711680, # لون أحمر للإنذار
    "description": f"**Found {len(new_findings)} New Vulnerability(ies)**\n\n**🤖 AI Triage & Analysis:**\n{ai_report[:1500]}", # قص النص إذا كان طويلاً جداً
    "footer": {"text": "Automated Recon & Scan Pipeline"}
}

data = {"embeds": [embed]}

response = requests.post(webhook_url, json=data)
if response.status_code in [200, 204]:
    print("[+] Successfully sent alert to Discord!")
else:
    print(f"[-] Failed to send to Discord. Status: {response.status_code}")
