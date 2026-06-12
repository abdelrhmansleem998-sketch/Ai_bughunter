import os
import subprocess
import requests
import shutil

print("[*] Starting Advanced Recon Process (v2)...")
os.makedirs("data", exist_ok=True)

if not os.path.exists("targets.txt") or os.path.getsize("targets.txt") == 0:
    print("[-] targets.txt not found or empty.")
    exit(1)

with open("targets.txt", "r") as f:
    targets = [line.strip() for line in f if line.strip()]

# 1. Subfinder & Httpx
subprocess.run("subfinder -dL targets.txt -silent | httpx -silent > data/live_targets.txt", shell=True)

# 2. crt.sh (Safely handled)
print("[*] Querying crt.sh...")
crt_results = set()
for target in targets:
    try:
        req = requests.get(f"https://crt.sh/?q=%.{target}&output=json", timeout=10)
        if req.status_code == 200:
            data = req.json()
            for entry in data:
                crt_results.add(entry.get('name_value', '').split('\n')[0])
    except Exception:
        print(f"[-] crt.sh failed for {target}, skipping.")
        continue

if crt_results:
    with open("data/crt_subs.txt", "w") as f:
        for sub in crt_results:
            f.write(sub + "\n")
    subprocess.run("cat data/crt_subs.txt | httpx -silent >> data/live_targets.txt", shell=True)
    subprocess.run("sort -u data/live_targets.txt -o data/live_targets.txt", shell=True)

# 3. Waybackurls & Katana (Crawling Live Targets)
print("[*] Fetching URLs (Wayback & Katana)...")
if os.path.exists("data/live_targets.txt"):
    subprocess.run("cat data/live_targets.txt | waybackurls > data/urls.txt", shell=True)
    # استخدام Katana للزحف الذكي
    subprocess.run("katana -list data/live_targets.txt -silent -depth 2 >> data/urls.txt", shell=True)
    subprocess.run("sort -u data/urls.txt -o data/urls.txt", shell=True)

# 4. Extract JS Files
if os.path.exists("data/urls.txt"):
    subprocess.run("cat data/urls.txt | grep -i '\.js$' > data/js_files.txt", shell=True)
    subprocess.run("sort -u data/js_files.txt -o data/js_files.txt", shell=True)

# 5. Whois & Dig (With Error Handling to prevent crashing)
print("[*] Running Whois & Dig...")
with open("data/dns_whois.txt", "w") as out:
    for target in targets:
        out.write(f"\n--- {target} ---\n")
        try:
            if shutil.which("whois"):
                whois_out = subprocess.run(["whois", target], capture_output=True, text=True, timeout=5).stdout
                out.write(whois_out + "\n")
            if shutil.which("dig"):
                dig_out = subprocess.run(["dig", target, "ANY"], capture_output=True, text=True, timeout=5).stdout
                out.write(dig_out + "\n")
        except Exception as e:
            out.write(f"Error gathering DNS info: {e}\n")

print("[+] Recon finished.")
