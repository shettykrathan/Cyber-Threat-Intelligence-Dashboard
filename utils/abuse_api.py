import requests
import os

def check_ip_abuse(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }
    headers = {
        "Key": os.getenv("ABUSE_API_KEY"),
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return {
            "abuseConfidenceScore": data["data"]["abuseConfidenceScore"],
            "totalReports": data["data"]["totalReports"]
        }
    return {"error": "Failed to fetch from AbuseIPDB"}
