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

try:
    with open("reports/latest_report.md", "r") as f:
        ai_report = f.read()
except FileNotFoundError:
    ai_report = "AI Report missing."

# إذا لم يقم الذكاء الاصطناعي بالرد، نكتفي بالثغرات
if ai_report == "NO_NEW_FINDINGS":
    exit(0)

# تجهيز الإشعار المرسل لـ Discord
embed = {
    "title": "🚨 AI BugHunter: New Vulnerabilities Detected!",
    "color": 16711680, 
    "description": f"**Found {len(new_findings)} New Vulnerability(ies)**\n\n**🤖 Groq AI Triage & Analysis:**\n\n{ai_report[:2000]}", 
    "footer": {"text": "Automated Bug Bounty Pipeline • github.com/projectdiscovery"}
}

data = {"embeds": [embed]}

try:
    response = requests.post(webhook_url, json=data)
    if response.status_code in [200, 204]:
        print("[+] Successfully sent alert to Discord!")
    else:
        print(f"[-] Failed to send to Discord. Status: {response.status_code}")
except Exception as e:
    print(f"[-] Error connecting to Discord Webhook: {e}")
