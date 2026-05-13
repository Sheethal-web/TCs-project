#!/bin/bash

# AWS Lambda Deployment Script for ML Recommendation Function
# This script packages the Lambda function and deploys it to AWS

set -e

# Configuration
FUNCTION_NAME="SmartAI-Recommendation"
REGION="us-east-1"  # Change this to your preferred region
ZIP_FILE="lambda_recommendation.zip"

echo "🚀 Starting Lambda deployment for $FUNCTION_NAME"

# Clean up any existing zip file
rm -f $ZIP_FILE

# Create deployment package
echo "📦 Creating deployment package..."
zip -r $ZIP_FILE lambda_recommendation.py massive_trained_rules.csv

echo "✅ Deployment package created: $ZIP_FILE"

# Check if function exists
if aws lambda get-function --function-name $FUNCTION_NAME --region $REGION >/dev/null 2>&1; then
    echo "🔄 Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
    echo "✅ Function updated successfully"
else
    echo "🆕 Creating new Lambda function..."

    # Create IAM role if it doesn't exist (you may need to adjust this)
    ROLE_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-recommendation-role"

    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime python3.9 \
        --role $ROLE_ARN \
        --handler lambda_recommendation.lambda_handler \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION \
        --description "Smart AI Product Recommendation Engine" \
        --timeout 30 \
        --memory-size 256

    echo "✅ Function created successfully"
fi

# Get the function ARN for API Gateway
FUNCTION_ARN=$(aws lambda get-function --function-name $FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text)
echo "🔗 Function ARN: $FUNCTION_ARN"

echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Create an API Gateway HTTP API or REST API"
echo "2. Add a POST method that integrates with this Lambda function"
echo "3. Update your frontend/backend to call the API Gateway URL instead of the local ML service"
echo ""
echo "Example API Gateway URL format:"
echo "https://your-api-id.execute-api.$REGION.amazonaws.com/prod/recommend"