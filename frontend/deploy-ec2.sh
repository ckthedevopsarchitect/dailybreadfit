#!/bin/bash

# DailyBreadFit Frontend Deployment Script for Ubuntu EC2
# Run this script on your EC2 instance after uploading the built files

echo "🚀 Setting up DailyBreadFit Frontend on EC2..."

# Install Nginx if not installed
sudo apt update
sudo apt install nginx -y

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/dailybread << 'EOF'
server {
    listen 80;
    server_name _;
    
    root /var/www/dailybread;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy API requests to backend (if running on same server)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Create web directory
sudo mkdir -p /var/www/dailybread

# Set permissions
sudo chown -R $USER:$USER /var/www/dailybread

# Enable the site
sudo ln -sf /etc/nginx/sites-available/dailybread /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "✅ Nginx configured successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Upload your build files: scp -r frontend/build/* user@ec2-ip:/var/www/dailybread/"
echo "2. Or copy locally: sudo cp -r /path/to/build/* /var/www/dailybread/"
echo "3. Visit: http://YOUR_EC2_PUBLIC_IP"
echo ""
echo "🔥 Firewall: Make sure port 80 is open in your EC2 Security Group!"
