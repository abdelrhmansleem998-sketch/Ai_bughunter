import os
import json
import requests

print("[*] Starting AI Analysis with Groq...")

groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    print("[-] GROQ_API_KEY not found in secrets.")
    exit(1)

# قراءة الثغرات الجديدة
try:
    with open("data/new_findings.json", "r") as f:
        new_findings = json.load(f)
except FileNotFoundError:
    new_findings = []

os.makedirs("reports", exist_ok=True)

if not new_findings:
    print("[*] No new findings to analyze.")
    with open("reports/latest_report.md", "w") as f:
        f.write("NO_NEW_FINDINGS")
    exit(0)

# تحويل الثغرات لنص ليفهمه الذكاء الاصطناعي
findings_text = json.dumps(new_findings, indent=2)

prompt = f"""
أنت خبير أمن سيبراني (Bug Bounty Hunter). تم اكتشاف الثغرات الجديدة التالية من خلال أداة Nuclei:
{findings_text}

المطلوب:
1. اكتب ملخصاً احترافياً قصيراً جداً لهذه الثغرات.
2. هل تعتقد أن هناك False Positives (إيجابيات كاذبة) محتملة بينها؟
3. ما هو التأثير الفعلي (Impact) لأخطر ثغرة فيهم؟
اكتب التقرير باللغة الإنجليزية وبشكل مختصر ومنسق لكي أرسله عبر Discord.
"""

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    ai_report = response.json()["choices"][0]["message"]["content"]
    
    with open("reports/latest_report.md", "w") as f:
        f.write(ai_report)
    print("[+] AI Analysis complete and saved.")
except Exception as e:
    print(f"[-] AI Analysis failed: {e}")
    with open("reports/latest_report.md", "w") as f:
        f.write("AI Analysis failed to generate. Please check raw findings in data/new_findings.json.")
