# Environment Configuration Guide

## Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# AWS Configuration
AWS_REGION=us-east-1

# DynamoDB Tables (automatically set by CDK deployment)
USERS_TABLE=dailybread-users
USER_PROFILES_TABLE=dailybread-user-profiles
RECIPES_TABLE=dailybread-recipes
DAILY_TIPS_TABLE=dailybread-daily-tips
USER_FAVORITES_TABLE=dailybread-user-favorites
ORDERS_TABLE=dailybread-orders
MEAL_PLANS_TABLE=dailybread-meal-plans

# S3 Buckets (automatically set by CDK deployment)
CONTENT_BUCKET=dailybread-content-ACCOUNT_ID
USER_UPLOADS_BUCKET=dailybread-user-uploads-ACCOUNT_ID

# Authentication
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30

# OpenAI API (for AI meal recommendations)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Stripe (for payments)
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
```

## Frontend Environment Variables

### Development (.env)
Create a `.env` file in the `frontend/` directory:

```bash
REACT_APP_API_URL=http://localhost:3001
```

### Production (.env.production)
```bash
REACT_APP_API_URL=https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod
```

## Lambda Environment Variables

These are automatically set by the CDK deployment, but you may need to add:

1. **OPENAI_API_KEY** - Required for AI meal recommendations
2. **JWT_SECRET_KEY** - For token signing/verification
3. **STRIPE_SECRET_KEY** - For payment processing

### Setting Lambda Environment Variables

```bash
# Using AWS CLI
aws lambda update-function-configuration \
  --function-name dailybread-auth \
  --environment Variables="{
    OPENAI_API_KEY=your-key,
    JWT_SECRET_KEY=your-secret,
    STRIPE_SECRET_KEY=your-stripe-key
  }"

aws lambda update-function-configuration \
  --function-name dailybread-meal-recommendations \
  --environment Variables="{
    OPENAI_API_KEY=your-key
  }"
```

### Using AWS Secrets Manager (Recommended for Production)

```bash
# Create secrets
aws secretsmanager create-secret \
  --name dailybread/openai-key \
  --secret-string "your-openai-api-key"

aws secretsmanager create-secret \
  --name dailybread/jwt-secret \
  --secret-string "your-jwt-secret-key"

aws secretsmanager create-secret \
  --name dailybread/stripe-secret \
  --secret-string "your-stripe-secret-key"
```

Then update Lambda to use Secrets Manager:
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# In your Lambda function
OPENAI_API_KEY = get_secret('dailybread/openai-key')
```

## Required API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save the key (you won't be able to see it again)

### Stripe API Keys
1. Go to https://stripe.com/
2. Sign up or log in
3. Navigate to Developers > API keys
4. Copy both Test and Live keys
5. Use Test keys for development, Live keys for production

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use different keys** for development and production
3. **Rotate keys regularly** (at least every 90 days)
4. **Use AWS Secrets Manager** for production secrets
5. **Enable CloudTrail** to audit secret access
6. **Limit IAM permissions** to least privilege
7. **Use strong, unique passwords** for JWT secrets

## Troubleshooting

### API not accessible
- Check CORS configuration in API Gateway
- Verify API endpoint URL in frontend `.env.production`
- Ensure Lambda functions have correct permissions

### Authentication errors
- Verify JWT_SECRET_KEY is the same across all Lambda functions
- Check token expiration settings
- Ensure proper error handling in auth middleware

### AI recommendations not working
- Verify OPENAI_API_KEY is set correctly
- Check OpenAI API quota and billing
- Review Lambda CloudWatch logs for errors
- Ensure Lambda has sufficient timeout (60s) and memory (1024MB)
