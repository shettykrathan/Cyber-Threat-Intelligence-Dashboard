import requests

def get_ip_score_numeric(ip):
    url = f"https://api.greynoise.io/v3/community/{ip}"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            classification = data.get("classification")

            # 🧠 Map classification to numeric score
            score_map = {
                "malicious": 100,
                "legitimate": 10,
                "unknown": 50
            }
            score = score_map.get(classification, 50)  # default to 50 if unknown

            return {
                "score": score,
                "label": classification
            }

        elif response.status_code == 404:
            return {
                "score": 50,
                "label": "unknown"
            }

        else:
            return {
                "error": True,
                "message": "GreyNoise API error",
                "status": response.status_code,
                "details": response.text
            }

    except Exception as e:
        return {"error": True, "message": str(e)}
