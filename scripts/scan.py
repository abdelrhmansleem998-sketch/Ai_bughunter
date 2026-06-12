import os
import subprocess

print("[*] Starting Comprehensive Vulnerability Scan with Nuclei...")

# تنظيف النتائج القديمة إن وجدت
if os.path.exists("data/nuclei_output.json"):
    os.remove("data/nuclei_output.json")

# 1. فحص الأهداف الأساسية (SQLi, XSS, CVEs, Misconfigs)
if os.path.exists("data/live_targets.txt") and os.path.getsize("data/live_targets.txt") > 0:
    print("[*] Scanning Live Targets...")
    subprocess.run("nuclei -l data/live_targets.txt -j -o data/nuclei_output.json -severity low,medium,high,critical", shell=True)
else:
    print("[-] No live targets to scan.")

# 2. فحص ملفات الـ JS لاكتشاف الأسرار (API Keys, Tokens)
if os.path.exists("data/js_files.txt") and os.path.getsize("data/js_files.txt") > 0:
    print("[*] Scanning JS Files for secrets and exposures...")
    subprocess.run("nuclei -l data/js_files.txt -t exposures/ -j -o data/nuclei_js.json", shell=True)
    
    # دمج نتائج الـ JS مع النتائج الأساسية
    if os.path.exists("data/nuclei_js.json"):
        subprocess.run("cat data/nuclei_js.json >> data/nuclei_output.json", shell=True)

print("[+] All Scans completed.")
