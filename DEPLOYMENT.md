# 🚀 Free Deployment Guide for CTI Dashboard

This guide will help you deploy your CTI Dashboard to free hosting platforms.

## 📋 Prerequisites

1. **GitHub Account** (free) - https://github.com
2. **MongoDB Atlas Account** (free tier) - https://www.mongodb.com/cloud/atlas
3. **API Keys** (if needed):
   - VirusTotal API key
   - GreyNoise API key

---

## 🌟 Option 1: Render (Recommended - Easiest)

### Step 1: Prepare Your Code

1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

### Step 2: Set Up MongoDB Atlas (Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0 - Free tier)
4. Create a database user
5. Whitelist IP: `0.0.0.0/0` (allow all IPs)
6. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### Step 3: Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `cti-dashboard` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add Environment Variables:
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: Generate a random secret key (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `VT_API_KEY`: Your VirusTotal API key (if needed)
   - `GN_API_KEY`: Your GreyNoise API key (if needed)
7. Click **"Create Web Service"**
8. Wait for deployment (5-10 minutes)

**Your app will be live at:** `https://your-app-name.onrender.com`

---

## 🌟 Option 2: Railway (Alternative)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway will auto-detect Python
6. Add Environment Variables:
   - `MONGO_URI`: Your MongoDB connection string
   - `SECRET_KEY`: Random secret key
   - `VT_API_KEY`: (if needed)
   - `GN_API_KEY`: (if needed)
7. Railway will automatically deploy

**Your app will be live at:** `https://your-app-name.up.railway.app`

---

## 🌟 Option 3: PythonAnywhere (Python-Specific)

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Sign up for free "Beginner" account

### Step 2: Upload Your Code

1. Go to **Files** tab
2. Upload your project files
3. Or use Git: **Consoles** → `git clone YOUR_REPO_URL`

### Step 3: Set Up Virtual Environment

1. Open **Consoles** → **Bash**
2. Run:
   ```bash
   cd your-project-folder
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Step 4: Configure Web App

1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **Flask** → **Python 3.10**
4. Set **Source code**: `/home/yourusername/your-project-folder`
5. Set **Working directory**: `/home/yourusername/your-project-folder`
6. Edit WSGI file:
   ```python
   import sys
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
7. Add environment variables in **Web** → **Environment variables**

### Step 5: Reload

Click **"Reload"** button

**Your app will be live at:** `https://yourusername.pythonanywhere.com`

---

## 🔧 Environment Variables Setup

For all platforms, you need to set these environment variables:

| Variable | Description | How to Get |
|----------|-------------|------------|
| `MONGO_URI` | MongoDB connection string | From MongoDB Atlas |
| `SECRET_KEY` | Flask secret key | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `VT_API_KEY` | VirusTotal API key | From VirusTotal account |
| `GN_API_KEY` | GreyNoise API key | From GreyNoise account |

---

## 📝 Important Notes

1. **Free Tier Limitations:**
   - Render: App sleeps after 15 mins of inactivity (wakes on first request)
   - Railway: 500 hours/month free, then $5/month
   - PythonAnywhere: Limited CPU time, no custom domains on free tier

2. **MongoDB Atlas Free Tier:**
   - 512 MB storage
   - Shared cluster
   - Perfect for development/testing

3. **Security:**
   - Never commit `.env` file to GitHub
   - Use environment variables in hosting platform
   - Change default `SECRET_KEY` in production

---

## 🐛 Troubleshooting

### App won't start
- Check build logs in your hosting platform
- Ensure all dependencies are in `requirements.txt`
- Verify environment variables are set correctly

### MongoDB connection fails
- Check MongoDB Atlas IP whitelist (should include `0.0.0.0/0`)
- Verify connection string format
- Check database user credentials

### Static files not loading
- Ensure `static/` folder is in repository
- Check file paths in templates (should use `url_for('static', ...)`)

---

## ✅ Quick Checklist

- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas cluster created
- [ ] Environment variables configured
- [ ] App deployed successfully
- [ ] Test login/signup functionality
- [ ] Test IP lookup feature

---

## 🎉 You're Live!

Once deployed, share your app URL with others. The free tier is perfect for:
- Personal projects
- Portfolio demonstrations
- Testing and development
- Small-scale applications

**Need help?** Check the hosting platform's documentation or community forums.

