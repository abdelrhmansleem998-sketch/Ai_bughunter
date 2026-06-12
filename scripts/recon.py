import os
import subprocess

print("[*] Starting Recon Process...")

# إنشاء مجلد data إذا لم يكن موجوداً
os.makedirs("data", exist_ok=True)

# التأكد من وجود ملف الأهداف
if not os.path.exists("targets.txt"):
    print("[-] targets.txt not found. Exiting.")
    exit(1)

# تشغيل Subfinder ثم تمرير النتائج إلى Httpx لمعرفة الأهداف التي تعمل
recon_command = "subfinder -dL targets.txt -silent | httpx -silent > data/live_targets.txt"
subprocess.run(recon_command, shell=True)

# التحقق من النتائج
if os.path.exists("data/live_targets.txt"):
    with open("data/live_targets.txt", "r") as f:
        targets = f.readlines()
    print(f"[+] Recon finished. Found {len(targets)} live endpoints.")
else:
    print("[-] Recon failed or no live targets found.")
