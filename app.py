from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from flask import Flask, render_template, request, Response
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from utils.vt_api import check_ip_virustotal
from utils.gn_api import get_ip_score_numeric
import csv
import io
last_result = None
load_dotenv()
app = Flask(__name__)
app.secret_key = 'supersecret'

# Configure MongoDB connection
# Read URI from env, default to local MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Determine whether to use TLS. For local connections (localhost/127.0.0.1) we disable TLS by default.
env_tls = os.getenv("MONGO_TLS")
use_tls = False
if env_tls is not None:
    use_tls = str(env_tls).lower() in ("1", "true", "yes", "on")
else:
    # Auto-enable TLS for SRV connection strings or explicit tls query params
    if "mongodb+srv" in mongo_uri or "tls=true" in mongo_uri.lower():
        use_tls = True

client = MongoClient(
    mongo_uri,
    tls=use_tls,
    serverSelectionTimeoutMS=5000
)
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


@app.route('/lookup', methods=['POST'])
def lookup():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global last_result

    ip = request.form['target']

    vt_data = check_ip_virustotal(ip)
    gn_data = get_ip_score_numeric(ip)

    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

    geo_response = requests.get(f"http://ip-api.com/json/{ip}").json()
    geo_info = {
        "country": geo_response.get("country", "Unknown"),
        "region": geo_response.get("regionName", "Unknown"),
        "city": geo_response.get("city", "Unknown"),
        "isp": geo_response.get("isp", "Unknown")
    }

    result = {
        "ip": ip,
        "timestamp": timestamp,
        "geo": geo_info,
        "virustotal": vt_data,
        "greynoise": gn_data,
    }

    threats_collection.insert_one(result)

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

    threats = list(threats_collection.find().sort("timestamp", -1))  
    return render_template('history.html', threats=threats)


@app.route("/export")
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    threats = list(threats_collection.find())

    def generate():
        data = csv.StringIO()
        writer = csv.writer(data)

        writer.writerow((
            "IP", "Timestamp", "Country", "Region", "City", "ISP",
            "GreyNoise Score", "GreyNoise Label", "VT Harmless", "VT Suspicious", "VT Malicious", "VT Timeout", "VT Undetected"
        ))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

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
                threat.get("greynoise", {}).get("score", ""),
                threat.get("greynoise", {}).get("label", ""),
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
    app.run(debug=True, port=5001)
