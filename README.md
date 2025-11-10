# 🛡️ Cyber Threat Intelligence Dashboard

> A real-time threat analysis dashboard built with Flask, MongoDB, and third-party threat intelligence APIs.  
> **Developed in association with 🤝 Elevate Labs.**

A modern web application for analyzing IP addresses using VirusTotal and GreyNoise threat intelligence APIs.

## ✨ Features

- 🔍 **IP Threat Analysis** - Analyze IP addresses for security threats using GreyNoise & VirusTotal
- 📊 **Visual Dashboards** - Interactive charts and data visualizations
- 📈 **Scan History** - Track and review previous IP scans
- 🛡️ **Multi-Source Intelligence** - VirusTotal + GreyNoise integration
- 🧠 **Real-time threat analysis** with malicious/suspicious/legitimate classification
- 🔐 **User Authentication** - Secure login/signup system
- 📥 **Data Export** - Export scan results to CSV
- 🎨 **Modern UI/UX** - Beautiful, responsive design
- 🗂️ **MongoDB-based data logging**

## 🧰 Tech Stack

| Layer         | Technologies Used                  |
|---------------|-------------------------------------|
| Backend       | Python, Flask                      |
| APIs          | GreyNoise, VirusTotal              |
| Database      | MongoDB                            |
| Frontend      | HTML, TailwindCSS, JavaScript      |
| Deployment    | Render, Railway, Localhost          |

## 🚀 Quick Start (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/shettykrathan/cti-dashboard.git
   cd cti-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```env
   MONGO_URI=your_mongodb_connection_string
   SECRET_KEY=your_secret_key_here
   VT_API_KEY=your_virustotal_api_key
   GN_API_KEY=your_greynoise_api_key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   Open http://localhost:5001 in your browser

## 🌐 Deployment

The application can be deployed locally or to a cloud platform of your choice. Make sure to:

1. Set up MongoDB (local or Atlas)
2. Configure environment variables
3. Install dependencies
4. Run the Flask application

Recommended platforms:
- Local development
- MongoDB Atlas (for database)
- Any Python-supporting cloud platform

## 📋 Requirements

- Python 3.11+
- MongoDB (MongoDB Atlas free tier recommended)
- VirusTotal API key (optional)
- GreyNoise API key (optional)

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URI` | Yes | MongoDB connection string |
| `SECRET_KEY` | Recommended | Flask secret key for sessions |
| `VT_API_KEY` | Optional | VirusTotal API key |
| `GN_API_KEY` | Optional | GreyNoise API key |
| `MONGO_TLS` | Optional | Enable TLS for MongoDB (true/false) |

For local MongoDB:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_TLS=false
```

For MongoDB Atlas:
```env
MONGO_URI=mongodb+srv://...
MONGO_TLS=true
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📁 Project Structure

```
CTI-Dashboard/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version
├── .env                 # Environment variables (create this)
├── SECURITY.md          # Security guidelines
├── users.json           # Local user database
├── static/
│   └── styles.css       # Shared CSS styles
├── templates/
│   ├── index.html       # Dashboard home
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── result.html      # Threat analysis results
│   ├── history.html     # Scan history
│   └── visuals.html     # Data visualizations
└── utils/
    ├── __init__.py      # Package initialization
    ├── vt_api.py        # VirusTotal API integration
    └── gn_api.py        # GreyNoise API integration (with smart scoring)

Screenshots:
├── Index.png            # Dashboard screenshot
├── Results.png          # Analysis results screenshot
└── Visuals.png         # Visualizations screenshot
```

## 🎯 Usage

1. **Sign Up** - Create a new account
2. **Login** - Access the dashboard
3. **Analyze IP** - Enter an IP address to scan
4. **View Results** - See detailed threat analysis
5. **Check History** - Review previous scans
6. **Export Data** - Download results as CSV

## �️ Threat Assessment

The dashboard uses multiple data points to assess IP threats:

### VirusTotal Analysis
- Harmless/Suspicious/Malicious counts
- Reputation scoring
- Multiple security vendor results

### GreyNoise Intelligence
- Classification (Benign/Suspicious/Malicious)
- RIOT status (common business services)
- Scanning behavior detection
- Threat scoring system:
  - Benign: 10-35 (green)
  - Suspicious: 40-70 (yellow)
  - Malicious: 71-100 (red)
  - No Data: Shows when IP is unknown

## 🔒 Security Notes

- Change default `SECRET_KEY` in production
- Never commit `.env` file to version control
- Use strong passwords for database access
- Keep API keys secure

## 🙌 Acknowledgements

- Built in collaboration with Elevate Labs
- Powered by GreyNoise and VirusTotal
- Inspired by real-world CTI analysis tools

## 📫 Contact

**Developer**: Krathan Shetty  
📧 [shettykrathann@gmail.com](mailto:shettykrathann@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/shettykrathan)

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

⭐ Feel free to fork, contribute, or raise issues! Security is a shared responsibility.

**Made with ❤️ for Cybersecurity Professionals**
