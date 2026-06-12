import os
import subprocess

print("[*] Starting Vulnerability Scan with Nuclei...")

if not os.path.exists("data/live_targets.txt") or os.path.getsize("data/live_targets.txt") == 0:
    print("[-] No live targets to scan. Exiting.")
    exit(0)

# تشغيل Nuclei وحفظ المخرجات كـ JSONL
# نستثني ثغرات الـ info لتقليل الإزعاج، نركز على low فأعلى
scan_command = "nuclei -l data/live_targets.txt -j -o data/nuclei_output.json -severity low,medium,high,critical"
subprocess.run(scan_command, shell=True)

print("[+] Scan completed.")
