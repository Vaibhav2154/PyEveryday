import sys
import re
import socket
import whois
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
VT_API_KEY = os.getenv("VT_API_KEY")

def check_https(url):
    return url.startswith("https://")

def check_url_structure(url):
    pattern = re.compile(
        r'^(https?:\/\/)?'              # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}' # domain
        r'(\/\S*)?$'                     # optional path
    )
    return bool(pattern.match(url))

def check_domain_info(domain):
    try:
        info = whois.whois(domain)
        registrar = info.registrar or "Unknown"
        creation_date = info.creation_date

        # Handle list or single datetime
        if isinstance(creation_date, list) and creation_date:
            creation_date = creation_date[0]
        if hasattr(creation_date, "strftime"):
            creation_date = creation_date.strftime("%Y-%m-%d")
        else:
            creation_date = "Unknown"

        return f"✅ Domain registered: {creation_date} (Registrar: {registrar})"
    except Exception as e:
        return f"⚠️ WHOIS lookup failed: {e}"

def check_virustotal(url):
    if not VT_API_KEY:
        return "⚠️ VirusTotal API key not found."

    api_url = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": VT_API_KEY}

    try:
        # Submit URL for scanning
        response = requests.post(api_url, headers=headers, data={"url": url})
        if response.status_code != 200:
            return f"⚠️ VirusTotal error: {response.status_code}"

        # Get analysis ID
        analysis_id = response.json()["data"]["id"]

        # Fetch analysis results
        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        result = requests.get(analysis_url, headers=headers).json()

        stats = result["data"]["attributes"]["stats"]

        if stats["malicious"] > 0:
            return f"❌ VirusTotal: {stats['malicious']} malicious detections found!"
        else:
            return "✅ VirusTotal: No malicious detections found."
    except Exception as e:
        return f"⚠️ VirusTotal check failed: {e}"


def scan_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path

    report_lines = [
        "=============================================",
        "          🔎 URL Security Report",
        "=============================================",
        f"\n🔎 Scanning URL: {url}\n"
    ]

    # HTTPS check
    if check_https(url):
        report_lines.append("✅ Uses HTTPS (secure protocol).")
    else:
        report_lines.append("❌ Does not use HTTPS (insecure).")

    # Structure check
    if check_url_structure(url):
        report_lines.append("✅ URL structure looks normal.")
    else:
        report_lines.append("❌ Suspicious-looking URL structure.")

    # Domain WHOIS
    report_lines.append(check_domain_info(domain))

    # VirusTotal
    report_lines.append(check_virustotal(url))

    # Final status
    report_lines.append("\n=============================================")
    if any("❌" in line for line in report_lines):
        report_lines.append("📊 Overall Status: UNSAFE 🔴")
    elif any("⚠️" in line for line in report_lines):
        report_lines.append("📊 Overall Status: SAFE (Unverified) 🟡")
    else:
        report_lines.append("📊 Overall Status: SAFE 🟢")
    report_lines.append("=============================================")

    return "\n".join(report_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python url_scan.py <url>")
    else:
        url = sys.argv[1]
        print(scan_url(url))
