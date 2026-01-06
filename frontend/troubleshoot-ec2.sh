#!/bin/bash

# Troubleshooting Script for DailyBreadFit Frontend
# Run this on your EC2 instance to diagnose issues

echo "🔍 DailyBreadFit Frontend Troubleshooting..."
echo ""

# Check 1: Nginx Status
echo "1️⃣ Checking Nginx status..."
sudo systemctl status nginx --no-pager | head -5
echo ""

# Check 2: Files in web directory
echo "2️⃣ Checking files in /var/www/dailybread..."
ls -lah /var/www/dailybread/ 2>/dev/null || echo "❌ Directory doesn't exist or is empty!"
echo ""

# Check 3: Nginx configuration
echo "3️⃣ Checking Nginx configuration..."
sudo nginx -t
echo ""

# Check 4: Port 80 listening
echo "4️⃣ Checking if port 80 is listening..."
sudo netstat -tlnp | grep :80 || sudo ss -tlnp | grep :80
echo ""

# Check 5: Nginx error logs
echo "5️⃣ Last 10 lines of Nginx error log..."
sudo tail -10 /var/log/nginx/error.log
echo ""

# Check 6: Nginx access logs
echo "6️⃣ Last 10 lines of Nginx access log..."
sudo tail -10 /var/log/nginx/access.log
echo ""

# Check 7: File permissions
echo "7️⃣ Checking file permissions..."
ls -la /var/www/dailybread/index.html 2>/dev/null || echo "❌ index.html not found!"
echo ""

# Check 8: Firewall status
echo "8️⃣ Checking UFW firewall..."
sudo ufw status
echo ""

echo "✅ Diagnostics complete!"
echo ""
echo "📋 Common issues:"
echo "   - No files in /var/www/dailybread → Copy build files"
echo "   - Port 80 not listening → Nginx not started"
echo "   - Permission denied → Run: sudo chown -R www-data:www-data /var/www/dailybread"
echo "   - EC2 Security Group → Make sure port 80 is open"
