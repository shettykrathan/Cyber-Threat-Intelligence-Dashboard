from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from flask import Flask, render_template, request, Response
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from utils.vt_api import check_ip_virustotal
from utils.abuse_api import check_ip_abuse
import csv
import io
last_scanned_ip = None
load_dotenv()
app = Flask(__name__)
app.secret_key = 'supersecret'  


# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.cti_dashboard
threats_collection = db["threats"]

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error="Username already exists")
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')
@app.route("/test_mongo")
def test_mongo():
    try:
        db.test.insert_one({"msg": "Mongo connected!"})
        return "MongoDB Insert Successful ✅"
    except Exception as e:
        return f"MongoDB Error ❌: {e}"

@app.route('/lookup', methods=['POST'])
def lookup():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global last_result

    ip = request.form['target']

    # VirusTotal and AbuseIPDB results
    vt_data = check_ip_virustotal(ip)
    abuse_data = check_ip_abuse(ip)

    # Timestamp
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # GeoIP Lookup
    geo_response = requests.get(f"http://ip-api.com/json/{ip}").json()
    geo_info = {
        "country": geo_response.get("country", "Unknown"),
        "region": geo_response.get("regionName", "Unknown"),
        "city": geo_response.get("city", "Unknown"),
        "isp": geo_response.get("isp", "Unknown")
    }

    # Final Result Object
    result = {
        "ip": ip,
        "timestamp": timestamp,
        "geo": geo_info,
        "virustotal": vt_data,
        "abuseipdb": abuse_data
    }

    # Save to MongoDB
    threats_collection.insert_one(result)

    # Store in global for /results route
    last_result = result

    return render_template('result.html', result=result)


@app.route('/visuals')
def visuals():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    raw_threats = list(threats_collection.find())
    for t in raw_threats:
        if '_id' in t:
            t['_id'] = str(t['_id'])
    return render_template('visuals.html', threats=raw_threats)


@app.route('/results', methods=['GET'])
def results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global last_result
    if not last_result:
        return "No recent result available. Please scan an IP first.", 400
    return render_template('result.html', result=last_result)


@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    threats = list(threats_collection.find().sort("timestamp", -1))  # latest first
    return render_template('history.html', threats=threats)


@app.route("/export")
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    threats = list(threats_collection.find())

    def generate():
        data = csv.StringIO()
        writer = csv.writer(data)

        # Write header
        writer.writerow((
            "IP", "Timestamp", "Country", "Region", "City", "ISP",
            "Abuse Score", "VT Harmless", "VT Suspicious", "VT Malicious", "VT Timeout", "VT Undetected"
        ))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # Write data rows
        for threat in threats:
            ip = threat.get("ip", "")
            timestamp = threat.get("timestamp", "")
            geo = threat.get("geo", {})
            vt = threat.get("virustotal", {}).get("last_analysis_stats", {})
            abuse = threat.get("abuseipdb", {})

            writer.writerow((
                ip,
                timestamp,
                geo.get("country", ""),
                geo.get("region", ""),
                geo.get("city", ""),
                geo.get("isp", ""),
                abuse.get("abuseConfidenceScore", ""),
                vt.get("harmless", ""),
                vt.get("suspicious", ""),
                vt.get("malicious", ""),
                vt.get("timeout", ""),
                vt.get("undetected", "")
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=threat_report.csv"}
    )


if __name__ == '__main__':
    app.run(debug=True)
