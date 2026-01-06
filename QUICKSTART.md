# Quick Start Guide - Daily Bread

Get your Daily Bread application running in 15 minutes!

## Prerequisites Check

```bash
# Check Node.js (need v18+)
node --version

# Check Python (need 3.11+)
python3 --version

# Check AWS CLI
aws --version

# Check if AWS is configured
aws sts get-caller-identity
```

If any command fails, install the missing tool first.

## 5-Minute Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd dailybreadfit

# 2. Install all dependencies
npm run install:all

# 3. Set up backend virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
deactivate
cd ..

# 4. Create frontend .env file
cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:3001
EOF

# 5. Start frontend
cd frontend
npm start
```

Your app should now be running at `http://localhost:3000`! 🎉

## 10-Minute AWS Deployment

```bash
# 1. Install AWS CDK globally
npm install -g aws-cdk

# 2. Configure AWS credentials (if not done)
aws configure

# 3. Create backend .env with API keys
cat > backend/.env << EOF
OPENAI_API_KEY=your_openai_key_here
JWT_SECRET_KEY=$(openssl rand -hex 32)
EOF

# 4. Deploy everything!
cd infrastructure
./deploy.sh
```

The script will output your CloudFront URL. Access your app there! 🚀

## Common Issues & Fixes

### "Command not found: cdk"
```bash
npm install -g aws-cdk
```

### "AWS credentials not configured"
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Format (json)
```

### "Node version too old"
```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### "Python version too old"
```bash
# On macOS with Homebrew
brew install python@3.11

# On Ubuntu
sudo apt update
sudo apt install python3.11
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Deployment fails
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check CDK bootstrap
cd infrastructure
cdk bootstrap

# Try deployment again
./deploy.sh
```

## What You Get After Deployment

After successful deployment, you'll have:

✅ **Live Web App** at your CloudFront URL
✅ **REST API** via API Gateway
✅ **Database** (7 DynamoDB tables)
✅ **Storage** (3 S3 buckets)
✅ **AI Recommendations** (if OpenAI key provided)

## First Steps After Deployment

1. **Open your app** using the CloudFront URL
2. **Create an account** - click "Sign Up"
3. **Fill in your profile** with fitness goals
4. **Get recommendations** - navigate to "Meal Recommendations"
5. **Enjoy!** 🎉

## Getting Your API Keys

### OpenAI (for AI recommendations)
1. Go to https://platform.openai.com/
2. Sign up / Log in
3. Go to API Keys section
4. Create new key
5. Copy and save it

### Stripe (optional, for payments)
1. Go to https://stripe.com/
2. Sign up / Log in
3. Go to Developers → API keys
4. Copy Test keys for development

## Updating Your Deployed App

### Update Frontend
```bash
cd frontend
npm run build

# Upload to S3
aws s3 sync build/ s3://YOUR_FRONTEND_BUCKET --delete

# Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DIST_ID \
  --paths "/*"
```

### Update Backend
```bash
cd backend
# Make your changes

# Redeploy
cd ../infrastructure
cdk deploy
```

## Cost Management

### Check Your Costs
```bash
# View current month's costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Set Up Billing Alerts
1. Go to AWS Console → Billing
2. Click "Budgets"
3. Create budget (e.g., $50/month)
4. Set up email alerts

## Cleanup / Delete Everything

```bash
cd infrastructure
cdk destroy

# Delete S3 buckets (manual)
aws s3 rb s3://YOUR_FRONTEND_BUCKET --force
aws s3 rb s3://YOUR_CONTENT_BUCKET --force
aws s3 rb s3://YOUR_UPLOADS_BUCKET --force
```

## Getting Help

- 📖 **Full Documentation**: See `docs/README.md`
- 🚀 **Deployment Guide**: See `docs/DEPLOYMENT.md`
- ⚙️ **Environment Setup**: See `docs/ENVIRONMENT.md`
- 📋 **Project Summary**: See `docs/PROJECT_SUMMARY.md`

## Architecture at a Glance

```
┌─────────────┐
│   Users     │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  CloudFront     │ (CDN)
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌───────┐  ┌──────────┐
│  S3   │  │   API    │
│(React)│  │ Gateway  │
└───────┘  └─────┬────┘
                 │
            ┌────┴─────┐
            ↓          ↓
      ┌─────────┐  ┌─────────┐
      │ Lambda  │  │ Lambda  │
      │  Auth   │  │  Meals  │
      └────┬────┘  └────┬────┘
           │            │
           └────┬───────┘
                ↓
         ┌──────────────┐
         │  DynamoDB    │
         └──────────────┘
```

## Next Steps

1. **Explore the code** - Browse `/frontend` and `/backend`
2. **Add features** - Implement recipes, orders, etc.
3. **Customize** - Update styling, branding
4. **Monitor** - Set up CloudWatch dashboards
5. **Scale** - Optimize as usage grows

---

**Questions?** Check the full documentation in the `/docs` folder!

**Happy coding!** 🎉🥗💪
