#!/bin/bash

# Deploy script for Daily Bread application

set -e

echo "=== Daily Bread Deployment Script ==="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed"
    exit 1
fi

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "Installing AWS CDK..."
    npm install -g aws-cdk
fi

# Get AWS account and region
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")

echo "AWS Account: $AWS_ACCOUNT"
echo "AWS Region: $AWS_REGION"

# Step 1: Install backend dependencies
echo ""
echo "Step 1: Installing backend dependencies..."
cd ../backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ../infrastructure

# Step 2: Install infrastructure dependencies
echo ""
echo "Step 2: Installing infrastructure dependencies..."
npm install

# Step 3: Bootstrap CDK (if not already done)
echo ""
echo "Step 3: Bootstrapping CDK..."
cdk bootstrap aws://$AWS_ACCOUNT/$AWS_REGION

# Step 4: Deploy infrastructure
echo ""
echo "Step 4: Deploying infrastructure..."
cdk deploy --require-approval never

# Step 5: Get outputs
echo ""
echo "Step 5: Getting stack outputs..."
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name DailyBreadStack \
    --query "Stacks[0].Outputs[?OutputKey=='APIEndpoint'].OutputValue" \
    --output text)

CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
    --stack-name DailyBreadStack \
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" \
    --output text)

FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name DailyBreadStack \
    --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" \
    --output text)

echo ""
echo "=== Deployment Information ==="
echo "API Endpoint: $API_ENDPOINT"
echo "CloudFront URL: https://$CLOUDFRONT_URL"
echo "Frontend Bucket: $FRONTEND_BUCKET"

# Step 6: Build and deploy frontend
echo ""
echo "Step 6: Building and deploying frontend..."
cd ../frontend

# Create .env file with API endpoint
cat > .env.production << EOF
REACT_APP_API_URL=$API_ENDPOINT
EOF

# Build frontend
npm run build

# Deploy to S3
aws s3 sync build/ s3://$FRONTEND_BUCKET --delete

# Invalidate CloudFront cache
DISTRIBUTION_ID=$(aws cloudfront list-distributions \
    --query "DistributionList.Items[?Origins.Items[0].DomainName=='$FRONTEND_BUCKET.s3.amazonaws.com'].Id" \
    --output text)

if [ ! -z "$DISTRIBUTION_ID" ]; then
    echo "Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id $DISTRIBUTION_ID \
        --paths "/*"
fi

echo ""
echo "=== Deployment Complete ==="
echo "Your application is now available at: https://$CLOUDFRONT_URL"
echo ""
echo "API Endpoint: $API_ENDPOINT"
echo ""
echo "Next steps:"
echo "1. Set up your domain in Route53 (optional)"
echo "2. Configure ACM certificate for HTTPS (optional)"
echo "3. Update CORS settings in API Gateway if needed"
echo "4. Set up monitoring and logging"
echo "5. Configure environment variables for Lambda functions"
