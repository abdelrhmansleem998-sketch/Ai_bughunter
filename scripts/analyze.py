import os
import json
import requests

print("[*] Starting AI Analysis (v2)...")

groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    print("[-] GROQ_API_KEY not found.")
    exit(1)

os.makedirs("reports", exist_ok=True)

try:
    with open("data/new_findings.json", "r") as f:
        new_findings = json.load(f)
except FileNotFoundError:
    new_findings = []

if not new_findings:
    print("[*] No new findings.")
    with open("reports/latest_report.md", "w") as f: f.write("NO_NEW_FINDINGS")
    exit(0)

# أخذ أول 40 ثغرة فقط كحد أقصى للذكاء الاصطناعي لمنع الـ Limit
limited_findings = new_findings[:40]
findings_text = json.dumps(limited_findings, indent=2)

prompt = f"""
You are an expert Bug Bounty hunter. Review these NEW vulnerabilities found by Nuclei:
{findings_text}

Task:
1. Provide a very concise, professional summary.
2. Flag any obvious False Positives.
3. State the impact of the highest severity finding.
Format cleanly with bullet points. Keep it under 1500 characters.
"""

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    ai_report = response.json()["choices"][0]["message"]["content"]
    with open("reports/latest_report.md", "w") as f: f.write(ai_report)
    print("[+] AI Analysis saved.")
except Exception as e:
    print(f"[-] AI failed: {e}")
    with open("reports/latest_report.md", "w") as f: f.write("AI Analysis failed.")
