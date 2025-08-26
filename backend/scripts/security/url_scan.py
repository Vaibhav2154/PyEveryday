import os
import sys
import argparse
import requests
import base64
import time


def scan_url(url: str) -> str:
    report = []
    report.append(f"🔎 Scanning URL: {url}")

    
    if url.startswith("https://"):
        report.append("✅ Uses HTTPS (secure protocol).")
    else:
        report.append("⚠️ Does not use HTTPS (insecure protocol).")

    
    if "@" in url or url.count("//") > 1:
        report.append("🚨 Suspicious URL structure detected.")
    else:
        report.append("✅ URL structure looks normal.")

    
    api_key = os.getenv("VT_API_KEY", "")
    if not api_key:
        report.append("⚠️ VirusTotal check skipped (no API key set).")
        return "\n".join(report)

    try:
        headers = {"x-apikey": api_key}

        
        vt_url = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(vt_url, headers=headers, data={"url": url}, timeout=10)

        if response.status_code == 200:
            url_id = response.json()["data"]["id"]

            
            time.sleep(2)

            
            analysis_url = f"https://www.virustotal.com/api/v3/analyses/{url_id}"
            analysis_response = requests.get(analysis_url, headers=headers, timeout=10)

            if analysis_response.status_code == 200:
                stats = analysis_response.json()["data"]["attributes"]["stats"]
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)

                if malicious > 0 or suspicious > 0:
                    report.append(f"🚨 VirusTotal: {malicious} malicious, {suspicious} suspicious detections.")
                else:
                    report.append("✅ VirusTotal: No malicious detections found.")
            else:
                report.append(f"⚠️ Failed to fetch VirusTotal report (HTTP {analysis_response.status_code}).")
        else:
            report.append(f"⚠️ Failed to submit URL to VirusTotal (HTTP {response.status_code}).")

    except requests.exceptions.RequestException as e:
        report.append(f"⚠️ VirusTotal check error: {e}")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="URL Scanner Utility")
    parser.add_argument("command", choices=["scan"], help="Action to perform")
    parser.add_argument("url", help="URL to scan")
    args = parser.parse_args()

    if args.command == "scan":
        result = scan_url(args.url)
        print(result)


if __name__ == "__main__":
    main()
