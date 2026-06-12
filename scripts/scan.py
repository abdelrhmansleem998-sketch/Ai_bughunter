import os
import subprocess

print("[*] Starting Scan Pipeline (v2)...")

if os.path.exists("data/nuclei_output.json"):
    os.remove("data/nuclei_output.json")

if os.path.exists("data/live_targets.txt") and os.path.getsize("data/live_targets.txt") > 0:
    # تم تغيير الـ Severity لمنع آلاف التنبيهات الكاذبة
    subprocess.run("nuclei -l data/live_targets.txt -j -o data/nuclei_output.json -severity medium,high,critical", shell=True)

if os.path.exists("data/js_files.txt") and os.path.getsize("data/js_files.txt") > 0:
    # التركيز على التوكنز والكونفيج فقط لتقليل الـ False Positives
    subprocess.run("nuclei -l data/js_files.txt -t exposures/tokens/ -t exposures/configs/ -j -o data/nuclei_js.json", shell=True)
    if os.path.exists("data/nuclei_js.json"):
        subprocess.run("cat data/nuclei_js.json >> data/nuclei_output.json", shell=True)

print("[+] Scans completed.")
