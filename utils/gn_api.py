import requests

def calculate_threat_score(data):
    """Calculate a threat score from 0-100 based on multiple GreyNoise data points."""
    base_score = 50  # Start at neutral
    
    # Get key indicators and print raw response for debugging
    print(f"GreyNoise Raw Response: {data}")
    
    classification = (data.get("classification") or "").lower()
    is_riot = data.get("riot", False)  # RIOT = common business service
    is_noise = data.get("noise", False)  # Noise = scanning activity
    
    # Print the extracted values
    print(f"Extracted values - Classification: {classification}, RIOT: {is_riot}, Noise: {is_noise}")
    
    # Adjust score based on classification
    if classification == "malicious":
        base_score = 85  # Start high for malicious
    elif classification == "legitimate":
        base_score = 15  # Start low for legitimate
    
    # Adjust for RIOT status (known good services)
    if is_riot:
        base_score = max(10, base_score - 30)  # Reduce score, but keep minimum
    
    # Adjust for noise (scanning behavior)
    if is_noise:
        base_score = min(90, base_score + 20)  # Increase score, but keep maximum
    
    # Map the classification to a human-readable label
    # Force "Benign" for RIOT services regardless of other factors
    if is_riot or classification == "legitimate":
        label = "Benign"
    elif classification == "malicious" or base_score > 70:
        label = "Malicious"
    else:
        label = "Suspicious"
    
    # Debug logging
    print(f"GreyNoise Debug - IP Classification: {classification}, RIOT: {is_riot}, Noise: {is_noise}, Score: {base_score}, Label: {label}")
    
    return base_score, label

def get_ip_score_numeric(ip):
    url = f"https://api.greynoise.io/v3/community/{ip}"
    headers = {"Accept": "application/json"}

    # Remove pre-check of known ranges - only use GreyNoise data

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            score, label = calculate_threat_score(data)
            return {
                "score": score,
                "label": label
            }

        elif response.status_code == 404:
            # No data available from GreyNoise
            print(f"GreyNoise: No data available for IP {ip}")
            return {
                "score": 0,
                "label": "No Data"
            }

        else:
            # API error - return no result instead of making assumptions
            print(f"GreyNoise API error for IP {ip}: {response.status_code}")
            return {
                "score": 0,
                "label": "No Data"
            }

    except Exception as e:
        # Connection/timeout error - return no result
        print(f"GreyNoise API connection error for IP {ip}: {str(e)}")
        return {
            "score": 0,
            "label": "No Data"
        }
