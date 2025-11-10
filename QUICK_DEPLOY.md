# ⚡ Quick Deploy Guide - 5 Minutes to Live!

## 🎯 Your Generated Secret Key
```
SECRET_KEY=e3ec9256a2acb8fdc8859de197c2e4708f0d3bef546df44f13db819b0f1c8ef1
```
**Save this!** You'll need it for deployment.

---

## 📋 Step-by-Step Deployment

### Step 1: Create GitHub Repository (2 minutes)

1. Go to: **https://github.com/new**
2. Repository name: `cti-dashboard` (or your choice)
3. **Make it Public** (or Private - your choice)
4. **DO NOT** check "Initialize with README"
5. Click **"Create repository"**

### Step 2: Push Your Code (1 minute)

Run these commands in your terminal (in the project folder):

```bash
git remote add origin https://github.com/YOUR_USERNAME/cti-dashboard.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

### Step 3: Set Up MongoDB Atlas (2 minutes)

1. Go to: **https://www.mongodb.com/cloud/atlas**
2. Click **"Try Free"** or **"Sign Up"**
3. Create account (use Google/GitHub for faster signup)
4. Create a **FREE** cluster (M0 - Free tier)
5. Wait 3-5 minutes for cluster to be created
6. Click **"Connect"** → **"Connect your application"**
7. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
8. Go to **"Network Access"** → **"Add IP Address"** → **"Allow Access from Anywhere"** (0.0.0.0/0)

### Step 4: Deploy to Render (2 minutes)

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest way)
4. Click **"New +"** → **"Web Service"**
5. Connect your GitHub account if not already connected
6. Select your repository: `cti-dashboard`
7. Configure:
   - **Name**: `cti-dashboard` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
8. Scroll down to **"Environment Variables"** and add:

   | Key | Value |
   |-----|-------|
   | `MONGO_URI` | Your MongoDB connection string from Step 3 |
   | `SECRET_KEY` | `e3ec9256a2acb8fdc8859de197c2e4708f0d3bef546df44f13db819b0f1c8ef1` |

9. Click **"Create Web Service"**
10. Wait 5-10 minutes for deployment

### Step 5: You're Live! 🎉

Your app will be available at:
**`https://cti-dashboard.onrender.com`** (or your custom name)

---

## 🔧 Troubleshooting

### If deployment fails:
1. Check **"Logs"** tab in Render dashboard
2. Verify environment variables are set correctly
3. Make sure MongoDB IP whitelist includes `0.0.0.0/0`

### If MongoDB connection fails:
1. Check connection string format
2. Verify database user credentials
3. Check IP whitelist in MongoDB Atlas

### If static files don't load:
- This should work automatically, but if not, check that `static/` folder is in your repo

---

## ✅ Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas cluster created
- [ ] MongoDB connection string copied
- [ ] Render account created
- [ ] Web service deployed on Render
- [ ] Environment variables set
- [ ] App is live and accessible

---

## 🎯 Quick Commands Reference

```bash
# Generate new secret key (if needed)
python -c "import secrets; print(secrets.token_hex(32))"

# Check git status
git status

# Push to GitHub
git push -u origin main

# View deployment logs (in Render dashboard)
# Go to your service → Logs tab
```

---

## 💡 Pro Tips

1. **Free Tier Limits:**
   - Render: App sleeps after 15 mins of inactivity (wakes on first request)
   - MongoDB: 512 MB storage (plenty for testing)

2. **Custom Domain:**
   - Render free tier supports custom domains
   - Add your domain in Render dashboard → Settings

3. **Auto-Deploy:**
   - Render auto-deploys on every git push
   - Just push to main branch and it updates!

---

**Need help?** Check the full guide in `DEPLOYMENT.md` or open an issue on GitHub!

