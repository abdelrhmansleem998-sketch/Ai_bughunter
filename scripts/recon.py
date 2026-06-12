import os
import subprocess
import requests

print("[*] Starting Advanced Recon Process...")
os.makedirs("data", exist_ok=True)

if not os.path.exists("targets.txt") or os.path.getsize("targets.txt") == 0:
    print("[-] targets.txt not found or empty. Exiting.")
    exit(1)

with open("targets.txt", "r") as f:
    targets = [line.strip() for line in f if line.strip()]

# 1. Subdomains & Live Hosts (Subfinder + Httpx)
print("[*] Running Subfinder & Httpx...")
subprocess.run("subfinder -dL targets.txt -silent | httpx -silent > data/live_targets.txt", shell=True)

# 2. crt.sh (Certificate Transparency)
print("[*] Querying crt.sh for additional subdomains...")
crt_results = set()
for target in targets:
    try:
        req = requests.get(f"https://crt.sh/?q=%.{target}&output=json", timeout=15)
        if req.status_code == 200:
            for entry in req.json():
                crt_results.add(entry['name_value'].split('\n')[0])
    except Exception as e:
        print(f"[-] crt.sh timeout/error for {target}")

if crt_results:
    with open("data/crt_subs.txt", "w") as f:
        for sub in crt_results:
            f.write(sub + "\n")
    # دمج دومينات crt.sh مع live_targets لزيادة مساحة الهجوم
    subprocess.run("cat data/crt_subs.txt | httpx -silent >> data/live_targets.txt", shell=True)
    subprocess.run("sort -u data/live_targets.txt -o data/live_targets.txt", shell=True)

# 3. Waybackurls (Archived Endpoints & Parameters)
print("[*] Fetching URLs from Wayback Machine...")
subprocess.run("cat targets.txt | waybackurls > data/wayback_urls.txt", shell=True)

# 4. Extract JS Files for Source Code Analysis
print("[*] Extracting JavaScript files...")
if os.path.exists("data/wayback_urls.txt"):
    subprocess.run("cat data/wayback_urls.txt | grep -i '\.js$' > data/js_files.txt", shell=True)
if os.path.exists("data/live_targets.txt"):
    subprocess.run("cat data/live_targets.txt | subjs >> data/js_files.txt", shell=True)
if os.path.exists("data/js_files.txt"):
    subprocess.run("sort -u data/js_files.txt -o data/js_files.txt", shell=True)

# 5. SSL/TLS Analysis (tlsx)
print("[*] Running Fast SSL/TLS analysis...")
if os.path.exists("data/live_targets.txt"):
    subprocess.run("tlsx -l data/live_targets.txt -silent -o data/ssl_results.txt", shell=True)

# 6. Basic DNS & Whois
print("[*] Running Whois & Dig...")
with open("data/dns_whois.txt", "w") as out:
    for target in targets:
        out.write(f"\n================ WHOIS: {target} ================\n")
        whois_out = subprocess.run(["whois", target], capture_output=True, text=True).stdout
        out.write(whois_out + "\n")
        out.write(f"\n================ DIG: {target} ================\n")
        dig_out = subprocess.run(["dig", target, "ANY"], capture_output=True, text=True).stdout
        out.write(dig_out + "\n")

print("[+] Advanced Recon finished. Data saved in /data folder.")
