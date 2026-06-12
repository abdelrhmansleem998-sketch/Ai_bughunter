# 🐞 AI BugHunter Pipeline

A fully automated, zero-cost, continuous Bug Bounty reconnaissance and vulnerability scanning pipeline. Powered by **GitHub Actions** for compute and **Groq AI (Llama 3.3)** for intelligent triage.

## 🧠 The Split Architecture (Security First)
This repository acts as the **Public Engine**. It utilizes GitHub's unlimited free compute minutes for public repositories. However, all sensitive data (Targets and Findings) are kept strictly confidential using a "Split Architecture" design.

* **The Engine (This Public Repo):** Runs the tools, Python scripts, and AI analysis. It leaves no trace of data once the job is finished.
* **The Vault (Private Repo):** A separate, hidden repository (`bughunter-data`) that stores `targets.txt` and the `findings.db` SQLite database.

## ⚙️ Core Features
* **Advanced Reconnaissance:** Discovers subdomains, live hosts, crt.sh logs, Wayback URLs, JavaScript files, and performs DNS/SSL scanning.
* **Vulnerability Scanning:** Uses Nuclei templates to find misconfigurations, CVEs, exposed panels, and hardcoded secrets in JS files.
* **Smart State Management:** An SQLite database tracks past findings to ensure you only get alerted for **new** discoveries (no duplicate spam).
* **AI Triage:** Groq AI (Llama 3.3) analyzes new findings, filters out potential false positives, and writes impact summaries.
* **Discord Alerts:** Real-time, neatly formatted webhook notifications directly to your server.

## 🛠️ Tools Arsenal
* `subfinder` & `httpx`
* `nuclei`
* `waybackurls` & `subjs`
* `tlsx`
* `whois` & `dig`

## 🚀 Setup Instructions

### 1. Create the Private Vault
1. Create a **Private** repository named `bughunter-data`.
2. Add a `targets.txt` file inside it containing your in-scope domains (one per line).

### 2. Configure Secrets
In this public repository, go to **Settings > Secrets and variables > Actions** and add the following repository secrets:
* `DATA_PAT`: A GitHub Personal Access Token (Classic) with full `repo` scope to allow the engine to access your private vault.
* `GROQ_API_KEY`: Your free API key from console.groq.com.
* `DISCORD_WEBHOOK_URL`: Your Discord channel webhook URL.

### 3. Run the Pipeline
Go to the **Actions** tab, select the `AI BugHunter Pipeline` workflow, and click **Run workflow**. 
The pipeline is also scheduled to run automatically every day at 02:00 AM UTC.

## ⚠️ Legal Disclaimer
This tool is designed strictly for authorized security testing and ethical hacking within official Bug Bounty programs (e.g., HackerOne, Bugcrowd, Intigriti). The author is not responsible for any misuse. Never point this tool at a target you do not have explicit, legal permission to test.
