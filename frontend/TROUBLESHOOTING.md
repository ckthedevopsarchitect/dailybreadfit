## 🚨 Frontend Not Showing - Troubleshooting Guide

### Quick Diagnostic Checklist

Run this on your EC2 instance:
```bash
# Upload and run troubleshooting script
chmod +x troubleshoot-ec2.sh
./troubleshoot-ec2.sh
```

---

## Most Common Issues

### ❌ Issue 1: Build Files Not Copied to Server

**Problem:** You ran deploy-ec2.sh but didn't copy the build files.

**Solution on EC2:**
```bash
# If you uploaded build files to /home/ubuntu/build
sudo cp -r /home/ubuntu/build/* /var/www/dailybread/

# Or if they're in a different location
sudo cp -r /path/to/your/build/* /var/www/dailybread/

# Fix permissions
sudo chown -R www-data:www-data /var/www/dailybread
sudo chmod -R 755 /var/www/dailybread
```

**Upload from your local machine:**
```bash
# From your Mac
cd /Users/ck/gitrepo/dailybreadfit/frontend
scp -i ~/.ssh/your-key.pem -r build/* ubuntu@YOUR_EC2_IP:/home/ubuntu/

# Then on EC2
sudo cp -r /home/ubuntu/* /var/www/dailybread/
```

---

### ❌ Issue 2: Wrong API URL in Build

**Problem:** Build doesn't have the correct backend API URL.

**Solution - Rebuild with correct API URL:**

**On your Mac:**
```bash
cd /Users/ck/gitrepo/dailybreadfit/frontend

# Edit .env.production with your EC2 IP
nano .env.production
# Change to: REACT_APP_API_URL=http://YOUR_EC2_PUBLIC_IP:8000

# Rebuild
npm run build

# Upload new build to EC2
scp -i ~/.ssh/your-key.pem -r build/* ubuntu@YOUR_EC2_IP:/home/ubuntu/
```

**Then on EC2:**
```bash
sudo rm -rf /var/www/dailybread/*
sudo cp -r /home/ubuntu/* /var/www/dailybread/
sudo systemctl restart nginx
```

---

### ❌ Issue 3: EC2 Security Group Blocks Port 80

**Problem:** AWS Security Group doesn't allow HTTP traffic.

**Solution - Check AWS Console:**
1. Go to EC2 → Instances → Your Instance
2. Click on Security Groups
3. Edit Inbound Rules
4. Add Rule:
   - Type: HTTP
   - Protocol: TCP
   - Port: 80
   - Source: 0.0.0.0/0 (anywhere)
5. Save

---

### ❌ Issue 4: Nginx Not Running

**Check on EC2:**
```bash
sudo systemctl status nginx

# If not running:
sudo systemctl start nginx
sudo systemctl enable nginx

# Check for errors:
sudo nginx -t
sudo tail -50 /var/log/nginx/error.log
```

---

### ❌ Issue 5: Wrong Nginx Root Directory

**Verify on EC2:**
```bash
# Check if files exist
ls -la /var/www/dailybread/

# Should show:
# index.html
# static/
# manifest.json
# etc.

# If empty, copy files:
sudo cp -r /path/to/build/* /var/www/dailybread/
```

---

### ❌ Issue 6: Browser Shows Blank Page

**Check browser console (F12):**
- **404 errors on JS/CSS:** Build paths are wrong
- **CORS errors:** Backend CORS not configured
- **Connection refused:** Backend not running

**Solution:**
```bash
# On EC2, check if index.html loads
curl http://localhost

# Check backend is running
curl http://localhost:8000/health || echo "Backend not running!"

# View browser console errors and share them for specific help
```

---

## Step-by-Step Verification

### 1. Check EC2 Instance is Accessible
```bash
# From your Mac
ping YOUR_EC2_PUBLIC_IP
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR_EC2_IP
```

### 2. Verify Nginx is Running on EC2
```bash
sudo systemctl status nginx
curl http://localhost
```

### 3. Check Files Exist
```bash
ls -la /var/www/dailybread/
cat /var/www/dailybread/index.html | head -5
```

### 4. Test from Browser
```
http://YOUR_EC2_PUBLIC_IP
```

### 5. Check Browser Console (F12)
Look for errors in:
- Console tab
- Network tab

---

## Quick Fix Commands

**Complete reset on EC2:**
```bash
# Stop nginx
sudo systemctl stop nginx

# Remove old files
sudo rm -rf /var/www/dailybread/*

# Recreate directory
sudo mkdir -p /var/www/dailybread

# Copy new build files (adjust path)
sudo cp -r /home/ubuntu/build/* /var/www/dailybread/

# Fix permissions
sudo chown -R www-data:www-data /var/www/dailybread
sudo chmod -R 755 /var/www/dailybread

# Restart nginx
sudo systemctl start nginx

# Check status
sudo systemctl status nginx
```

**Check what's actually being served:**
```bash
curl -I http://localhost
curl http://localhost | head -20
```

---

## Next Steps

**Tell me:**
1. What do you see when you visit `http://YOUR_EC2_IP` in browser?
   - Blank page?
   - Nginx welcome page?
   - 404 error?
   - Connection timeout?

2. Run on EC2 and share output:
```bash
ls -la /var/www/dailybread/
sudo systemctl status nginx
curl http://localhost
```

3. Browser console errors (Press F12, check Console tab)

This will help me pinpoint the exact issue!
