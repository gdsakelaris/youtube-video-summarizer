# YouTube Video Summarizer - Deployment Guide

## 🚀 Deploy to Render (Recommended - Free)

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it `youtube-video-summarizer`
3. Initialize your local repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/youtube-video-summarizer.git
   git push -u origin main
   ```

### Step 2: Deploy to Render

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `youtube-video-summarizer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### Step 3: Set Environment Variables

In Render dashboard, go to Environment:

- Add variable: `OPENAI_API_KEY` = `your_openai_api_key_here`
- Add variable: `FLASK_ENV` = `production`

### Step 4: Deploy!

Click "Deploy" and wait 5-10 minutes. Your app will be live at:
`https://your-app-name.onrender.com`

---

## 🌐 Alternative: Deploy to Railway

### Step 1: Create Railway Account

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Deploy

1. Click "New Project" → "Deploy from GitHub repo"
2. Select your repository
3. Railway auto-detects it's a Python app

### Step 3: Environment Variables

In Railway dashboard:

- Add `OPENAI_API_KEY` = `your_api_key`
- Add `FLASK_ENV` = `production`

### Step 4: Custom Domain (Optional)

- Railway provides a free `.railway.app` domain
- You can add a custom domain in the settings

---

## 💰 Alternative: Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to [PythonAnywhere.com](https://pythonanywhere.com)
2. Sign up for free account (includes web app hosting)

### Step 2: Upload Files

1. Use the file manager to upload your project files
2. Or clone from GitHub using console

### Step 3: Create Web App

1. Go to Web tab → "Add a new web app"
2. Choose Flask
3. Set up your app with the uploaded files

### Step 4: Install Requirements

In console:

```bash
pip3.10 install --user -r requirements.txt
```

---

## 🔒 Important Security Notes

1. **Never commit API keys** to GitHub
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** (most platforms do this automatically)
4. **Monitor usage** to avoid unexpected OpenAI costs

---

## 🌍 Your App Will Be Live!

Once deployed, anyone can access your YouTube Video Summarizer at your public URL! Share it with friends and colleagues.

## 📊 Monitoring & Analytics

- **Render**: Built-in metrics and logs
- **Railway**: Usage analytics in dashboard
- **PythonAnywhere**: Basic usage stats

## 🚀 Next Steps

- Add a custom domain
- Implement user authentication
- Add usage limits
- Create API endpoints
- Add more video platforms
