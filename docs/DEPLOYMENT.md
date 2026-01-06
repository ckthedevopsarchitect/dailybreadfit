# Deployment Guide

## Prerequisites

Before deploying, ensure you have:

- [x] AWS Account with appropriate permissions
- [x] AWS CLI installed and configured
- [x] Node.js (v18+) and npm installed
- [x] Python 3.11+ installed
- [x] AWS CDK CLI installed (`npm install -g aws-cdk`)
- [x] Git installed

## Pre-Deployment Checklist

- [ ] Configure AWS credentials
- [ ] Set up environment variables
- [ ] Review and update configuration files
- [ ] Test locally
- [ ] Obtain API keys (OpenAI, Stripe)

## Step-by-Step Deployment

### 1. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter output format (json)
```

Verify configuration:
```bash
aws sts get-caller-identity
```

### 2. Clone and Set Up Repository

```bash
git clone <repository-url>
cd dailybreadfit
```

### 3. Install Dependencies

```bash
# Install all project dependencies
npm run install:all
```

### 4. Set Up Backend Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 5. Configure Environment Variables

Create `.env` file in `backend/` directory:
```bash
# See docs/ENVIRONMENT.md for complete list
OPENAI_API_KEY=your_key_here
JWT_SECRET_KEY=your_secret_here
STRIPE_SECRET_KEY=your_stripe_key_here
```

### 6. Bootstrap AWS CDK

```bash
cd ../infrastructure

# Bootstrap CDK (first time only)
export AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export AWS_REGION=$(aws configure get region)

cdk bootstrap aws://$AWS_ACCOUNT/$AWS_REGION
```

### 7. Deploy Infrastructure

#### Option A: Automated Deployment (Recommended)

```bash
./deploy.sh
```

#### Option B: Manual Deployment

```bash
# Synthesize CloudFormation template
cdk synth

# Review changes
cdk diff

# Deploy
cdk deploy --require-approval never

# Get outputs
aws cloudformation describe-stacks \
  --stack-name DailyBreadStack \
  --query "Stacks[0].Outputs"
```

### 8. Configure Lambda Environment Variables

```bash
# Update Lambda functions with API keys
aws lambda update-function-configuration \
  --function-name dailybread-auth \
  --environment Variables="{
    JWT_SECRET_KEY=$JWT_SECRET_KEY,
    OPENAI_API_KEY=$OPENAI_API_KEY,
    STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
  }"

aws lambda update-function-configuration \
  --function-name dailybread-meal-recommendations \
  --environment Variables="{
    OPENAI_API_KEY=$OPENAI_API_KEY
  }"
```

### 9. Build and Deploy Frontend

```bash
cd ../frontend

# Get API endpoint from CDK output
API_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name DailyBreadStack \
  --query "Stacks[0].Outputs[?OutputKey=='APIEndpoint'].OutputValue" \
  --output text)

# Create production environment file
cat > .env.production << EOF
REACT_APP_API_URL=$API_ENDPOINT
EOF

# Build frontend
npm run build

# Get frontend bucket name
FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name DailyBreadStack \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" \
  --output text)

# Upload to S3
aws s3 sync build/ s3://$FRONTEND_BUCKET --delete

# Invalidate CloudFront cache
CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
  --stack-name DailyBreadStack \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" \
  --output text)

DISTRIBUTION_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?DomainName=='$CLOUDFRONT_URL'].Id" \
  --output text)

aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*"
```

### 10. Verify Deployment

```bash
# Test API endpoint
curl $API_ENDPOINT/auth/login

# Access frontend
echo "Frontend URL: https://$CLOUDFRONT_URL"
```

## Post-Deployment Configuration

### 1. Set Up Custom Domain (Optional)

#### Create Hosted Zone in Route53
```bash
aws route53 create-hosted-zone \
  --name dailybread.com \
  --caller-reference $(date +%s)
```

#### Request SSL Certificate
```bash
aws acm request-certificate \
  --domain-name dailybread.com \
  --domain-name www.dailybread.com \
  --validation-method DNS \
  --region us-east-1
```

#### Update CloudFront Distribution
```bash
# Add certificate and custom domain to CloudFront
aws cloudfront update-distribution \
  --id $DISTRIBUTION_ID \
  --distribution-config file://cloudfront-config.json
```

### 2. Configure API Gateway Custom Domain

```bash
# Create custom domain
aws apigateway create-domain-name \
  --domain-name api.dailybread.com \
  --certificate-arn $CERTIFICATE_ARN \
  --endpoint-configuration types=EDGE

# Create base path mapping
aws apigateway create-base-path-mapping \
  --domain-name api.dailybread.com \
  --rest-api-id $API_ID \
  --stage prod
```

### 3. Set Up Monitoring

```bash
# Enable CloudWatch Logs for API Gateway
aws apigateway update-stage \
  --rest-api-id $API_ID \
  --stage-name prod \
  --patch-operations \
    op=replace,path=/accessLogSettings/destinationArn,value=$LOG_GROUP_ARN

# Create CloudWatch Alarms
aws cloudwatch put-metric-alarm \
  --alarm-name dailybread-api-errors \
  --alarm-description "Alert when API error rate is high" \
  --metric-name 5XXError \
  --namespace AWS/ApiGateway \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 10
```

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Install dependencies
        run: |
          npm install -g aws-cdk
          cd infrastructure && npm install
      
      - name: Deploy infrastructure
        run: |
          cd infrastructure
          cdk deploy --require-approval never
      
      - name: Build and deploy frontend
        run: |
          cd frontend
          npm install
          npm run build
          aws s3 sync build/ s3://$FRONTEND_BUCKET --delete
```

## Rollback Procedures

### Rollback Infrastructure
```bash
cd infrastructure

# Revert to previous version
git checkout <previous-commit-hash>

# Deploy previous version
cdk deploy --require-approval never
```

### Rollback Frontend
```bash
# List previous S3 versions
aws s3api list-object-versions \
  --bucket $FRONTEND_BUCKET \
  --prefix index.html

# Restore previous version
aws s3api copy-object \
  --copy-source "$FRONTEND_BUCKET/index.html?versionId=<version-id>" \
  --bucket $FRONTEND_BUCKET \
  --key index.html
```

## Troubleshooting

### Deployment fails with permission errors
- Verify AWS credentials have sufficient permissions
- Check IAM role policies
- Ensure CDK bootstrap was successful

### Lambda function errors
- Check CloudWatch Logs
- Verify environment variables are set
- Check Lambda execution role permissions
- Verify layer compatibility

### Frontend not loading
- Check S3 bucket permissions
- Verify CloudFront distribution is active
- Check API endpoint in `.env.production`
- Clear browser cache

### API Gateway returns 502/504 errors
- Check Lambda function logs
- Verify Lambda timeout settings
- Check DynamoDB table permissions
- Verify network configuration (VPC, Security Groups)

## Clean Up / Destroy Resources

```bash
# Delete all resources
cd infrastructure
cdk destroy

# Empty and delete S3 buckets (if retained)
aws s3 rm s3://$FRONTEND_BUCKET --recursive
aws s3 rb s3://$FRONTEND_BUCKET

aws s3 rm s3://$CONTENT_BUCKET --recursive
aws s3 rb s3://$CONTENT_BUCKET
```

## Cost Optimization

1. **Enable S3 Lifecycle Policies** for old content
2. **Use CloudWatch Logs retention policies**
3. **Monitor DynamoDB capacity** (PAY_PER_REQUEST vs PROVISIONED)
4. **Enable Lambda reserved concurrency** for predictable costs
5. **Use CloudFront caching** to reduce origin requests
6. **Set up AWS Budgets** for cost alerts

## Security Checklist

- [ ] Enable CloudTrail for audit logging
- [ ] Set up AWS Config for compliance monitoring
- [ ] Enable GuardDuty for threat detection
- [ ] Configure AWS WAF for API Gateway
- [ ] Enable MFA for root account
- [ ] Use IAM roles with least privilege
- [ ] Encrypt data at rest (S3, DynamoDB)
- [ ] Use HTTPS everywhere
- [ ] Regularly rotate secrets
- [ ] Enable S3 bucket versioning
- [ ] Configure VPC Flow Logs (if using VPC)
