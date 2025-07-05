import requests
import os

def check_ip_virustotal(ip):
    headers = {
        "x-apikey": os.getenv("VT_API_KEY")
    }
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "last_analysis_stats": data["data"]["attributes"]["last_analysis_stats"],
            "reputation": data["data"]["attributes"].get("reputation", 0)
        }
    return {"error": "Failed to fetch from VirusTotal"}
