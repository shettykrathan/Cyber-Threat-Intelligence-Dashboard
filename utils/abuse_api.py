import requests
import os

def check_ip_abuse(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": os.getenv("ABUSE_API_KEY"),
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    # 🔐 Check if API key is missing
    if not headers["Key"]:
        print("❌ ABUSE_API_KEY is missing in environment variables.")
        return {"error": True, "message": "ABUSE_API_KEY not set"}

    try:
        print(f"📡 Calling AbuseIPDB for IP: {ip}")
        response = requests.get(url, headers=headers, params=params)
        print(f"📦 Status Code: {response.status_code}")
        print(f"📦 Response Text: {response.text[:300]}")  # Log first 300 chars

        if response.status_code == 200:
            data = response.json()
            return {
                "abuseConfidenceScore": data["data"]["abuseConfidenceScore"],
                "totalReports": data["data"]["totalReports"]
            }
        else:
            return {
                "error": True,
                "status": response.status_code,
                "message": "AbuseIPDB returned an error",
                "details": response.text
            }

    except Exception as e:
        print("❌ Exception while calling AbuseIPDB:", e)
        return {"error": True, "message": str(e)}
