import os
import json
import requests

print("[*] Starting AI Analysis with Groq...")

groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    print("[-] GROQ_API_KEY not found in secrets.")
    exit(1)

os.makedirs("reports", exist_ok=True)

try:
    with open("data/new_findings.json", "r") as f:
        new_findings = json.load(f)
except FileNotFoundError:
    new_findings = []

if not new_findings:
    print("[*] No new findings to analyze.")
    with open("reports/latest_report.md", "w") as f:
        f.write("NO_NEW_FINDINGS")
    exit(0)

# تجهيز البيانات للذكاء الاصطناعي
findings_text = json.dumps(new_findings, indent=2)

prompt = f"""
أنت خبير أمن سيبراني (Bug Bounty Hunter). تم اكتشاف الثغرات الجديدة التالية بواسطة أداة Nuclei:
{findings_text}

المطلوب بدقة:
1. اكتب ملخصاً احترافياً وسريعاً لهذه الثغرات.
2. حدد احتمالية أن تكون هذه الثغرات إيجابيات كاذبة (False Positives).
3. اذكر التأثير الفعلي (Impact) لأخطر ثغرة تم اكتشافها.
* الرجاء كتابة التقرير باللغة الإنجليزية، وأن يكون مختصراً ومنسقاً بنقاط (Bullet points) ليكون جاهزاً للإرسال عبر Discord.
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
        f.write("AI Analysis failed to generate. Raw findings are saved in data/new_findings.json.")
