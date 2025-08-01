# Deploy YouTube Video Summarizer to AWS EC2

## 🚀 Step 1: Launch EC2 Instance

### 1.1 Create EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose **Ubuntu Server 22.04 LTS** (free tier eligible)
4. Instance type: **t2.micro** (free tier)
5. Create new key pair (download the .pem file)
6. Security Group: Allow SSH (22), HTTP (80), HTTPS (443), Custom TCP (5000)
7. Launch instance

### 1.2 Connect to Instance

```bash
# Replace with your .pem file and instance IP
ssh -i your-key.pem ubuntu@your-ec2-ip
```

## 🔧 Step 2: Setup Environment

### 2.1 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 Install Python and Dependencies

```bash
# Install Python and pip
sudo apt install python3 python3-pip python3-venv git nginx -y

# Install PM2 for process management
sudo npm install -g pm2
```

### 2.3 Clone Your Repository

```bash
git clone https://github.com/YOUR_USERNAME/youtube-video-summarizer.git
cd youtube-video-summarizer
```

### 2.4 Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.5 Setup Environment Variables

```bash
# Create .env file
nano .env
```

Add this content:

```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=production
```

## 🚀 Step 3: Run the Application

### 3.1 Test the App

```bash
# Test locally first
python app.py
# Should show: Running on http://0.0.0.0:5000
```

### 3.2 Setup Process Manager

```bash
# Create PM2 ecosystem file
nano ecosystem.config.js
```

Add this content:

```javascript
module.exports = {
	apps: [
		{
			name: "youtube-summarizer",
			script: "venv/bin/gunicorn",
			args: "--bind 0.0.0.0:5000 --workers 2 app:app",
			cwd: "/home/ubuntu/youtube-video-summarizer",
			env: {
				FLASK_ENV: "production",
			},
		},
	],
};
```

### 3.3 Start with PM2

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🌐 Step 4: Setup Nginx (Optional but Recommended)

### 4.1 Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/youtube-summarizer
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or your EC2 public IP

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.2 Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/youtube-summarizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Step 5: Security & SSL (Optional)

### 5.1 Install Certbot for SSL

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 5.2 Setup Firewall

```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 🎯 Step 6: Access Your App

Your app will be available at:

- **HTTP**: `http://your-ec2-public-ip`
- **HTTPS**: `https://your-domain.com` (if SSL configured)

## 📊 Step 7: Monitor & Maintain

### View Logs

```bash
pm2 logs youtube-summarizer
```

### Restart App

```bash
pm2 restart youtube-summarizer
```

### Update App

```bash
cd youtube-video-summarizer
git pull
pm2 restart youtube-summarizer
```

## 💡 Tips for YouTube IP Issues

### 1. Try Different Regions

Launch EC2 in different regions:

- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)

### 2. Use Elastic IP

Get a dedicated IP address:

```bash
# In AWS Console: EC2 → Elastic IPs → Allocate
```

### 3. Rotate User-Agent (if needed)

Add this to your app.py if still blocked:

```python
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# Use random user agent
os.environ['USER_AGENT'] = random.choice(user_agents)
```

## 💰 Cost Estimate

- **t2.micro**: Free tier (750 hours/month)
- **Storage**: ~$1-2/month for 8GB
- **Data transfer**: Usually free for small apps
- **Total**: ~$0-5/month

## 🚨 Important Notes

1. **Security**: Keep your .pem file safe
2. **Monitoring**: Set up CloudWatch alarms
3. **Backups**: Regular snapshots of your instance
4. **Updates**: Keep system and packages updated
