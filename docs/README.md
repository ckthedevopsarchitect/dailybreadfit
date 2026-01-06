# Daily Bread - Nutrition & Meal Planning Application

A comprehensive web application that provides users with daily fitness tips, nutritious recipes, and AI-powered meal recommendations tailored to individual fitness goals.

## 🚀 Features

### Core Features
- **User Registration & Authentication** - Secure JWT-based authentication
- **User Profile Management** - Track fitness goals, dietary preferences, and body metrics
- **AI-Powered Meal Recommendations** - Personalized meal suggestions based on user profile
- **Daily Tips & Recipes** - Access to curated health tips and recipes
- **Favorites & History Tracking** - Save and track favorite meals and recipes
- **Meal Ordering System** - Order healthy, nutritious meals for delivery
- **Analytics Dashboard** - Track nutrition intake and progress

### Technical Features
- **Responsive Design** - Mobile and desktop optimized
- **Real-time Updates** - Live notifications for daily tips
- **SEO Optimized** - Built-in SEO best practices
- **Security** - Data encryption, secure APIs, JWT authentication
- **Scalable Architecture** - Serverless architecture on AWS

## 📋 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query (@tanstack/react-query)
- **Routing**: React Router v7
- **HTTP Client**: Axios
- **UI Components**: Headless UI, Hero Icons

### Backend
- **Language**: Python 3.11
- **Framework**: Lambda functions
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **AI Integration**: OpenAI GPT-4 for meal recommendations

### Databases
- **Primary Database**: Amazon DynamoDB
- **Tables**:
  - Users
  - User Profiles
  - Recipes
  - Daily Tips
  - User Favorites
  - Orders
  - Meal Plans

### AWS Infrastructure
- **Compute**: AWS Lambda
- **API**: API Gateway (REST API)
- **Storage**: Amazon S3
  - Frontend hosting
  - Content storage (images, assets)
  - User uploads
- **CDN**: CloudFront
- **DNS**: Route53
- **SSL/TLS**: AWS Certificate Manager (ACM)
- **IAM**: Role-based access control

### Infrastructure as Code
- **Tool**: AWS CDK (TypeScript)
- **Version**: 2.117.0

## 📁 Project Structure

```
dailybreadfit/
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── api/              # API client and endpoints
│   │   ├── components/       # Reusable React components
│   │   ├── contexts/         # React contexts (Auth, etc.)
│   │   ├── pages/            # Page components
│   │   ├── types/            # TypeScript type definitions
│   │   ├── App.tsx           # Main app component
│   │   └── index.tsx         # Entry point
│   ├── public/               # Static assets
│   └── package.json
│
├── backend/                   # Python backend
│   ├── functions/            # Lambda function handlers
│   │   ├── auth_handler.py   # Authentication endpoints
│   │   └── meal_recommendations.py  # AI meal recommendations
│   ├── auth.py               # Authentication utilities
│   ├── config.py             # Configuration settings
│   ├── database.py           # DynamoDB client utilities
│   ├── schema.py             # Database schema definitions
│   ├── requirements.txt      # Python dependencies
│   └── requirements-dev.txt  # Development dependencies
│
├── infrastructure/            # AWS CDK infrastructure
│   ├── bin/
│   │   └── app.ts            # CDK app entry point
│   ├── lib/
│   │   └── dailybread-stack.ts  # Main stack definition
│   ├── cdk.json              # CDK configuration
│   ├── deploy.sh             # Deployment script
│   └── package.json
│
├── docs/                      # Documentation
├── .gitignore
├── package.json              # Root package.json
└── README.md
```

## 🛠️ Setup & Installation

### Prerequisites
- Node.js (v18 or higher)
- Python 3.11 or higher
- AWS CLI configured with appropriate credentials
- AWS CDK CLI (`npm install -g aws-cdk`)

### Local Development

#### 1. Clone the repository
```bash
git clone <repository-url>
cd dailybreadfit
```

#### 2. Install dependencies
```bash
# Install all dependencies
npm run install:all
```

#### 3. Set up backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 4. Set up environment variables

Create a `.env` file in the `backend/` directory:
```bash
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=your_secret_key_change_in_production
STRIPE_SECRET_KEY=your_stripe_secret_key
```

Create a `.env` file in the `frontend/` directory:
```bash
REACT_APP_API_URL=http://localhost:3001
```

#### 5. Run frontend locally
```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

## 🚀 Deployment

### Deploy to AWS

#### Option 1: Automated Deployment
```bash
cd infrastructure
./deploy.sh
```

This script will:
1. Install backend dependencies
2. Install infrastructure dependencies
3. Bootstrap CDK (if needed)
4. Deploy infrastructure
5. Build and deploy frontend to S3
6. Invalidate CloudFront cache

#### Option 2: Manual Deployment

1. **Bootstrap CDK** (first time only):
```bash
cd infrastructure
cdk bootstrap
```

2. **Deploy infrastructure**:
```bash
cdk deploy
```

3. **Build and deploy frontend**:
```bash
cd ../frontend
npm run build

# Upload to S3
aws s3 sync build/ s3://YOUR_FRONTEND_BUCKET --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

### Post-Deployment Configuration

1. **Update API endpoint** in frontend `.env.production`:
```bash
REACT_APP_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/prod
```

2. **Configure custom domain** (optional):
   - Create hosted zone in Route53
   - Request SSL certificate in ACM
   - Update CloudFront distribution with custom domain
   - Add DNS records in Route53

3. **Set Lambda environment variables**:
   - OPENAI_API_KEY
   - JWT_SECRET_KEY
   - STRIPE_SECRET_KEY

## 📝 API Documentation

### Authentication Endpoints

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe",
  "fitness_goal": "weight_loss",
  "height": 175,
  "weight": 80,
  "age": 30,
  "gender": "male",
  "activity_level": "moderate"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

### Meal Recommendations

#### Get AI-Powered Recommendations
```http
POST /meals/recommendations
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "meal_type": "lunch"
}
```

Response:
```json
{
  "meal_type": "lunch",
  "recommendations": [
    {
      "name": "Grilled Chicken Salad",
      "description": "Fresh mixed greens with grilled chicken",
      "ingredients": ["Chicken breast", "Mixed greens", "Cherry tomatoes"],
      "nutrition": {
        "calories": 450,
        "protein": 45,
        "carbs": 30,
        "fat": 15
      },
      "prep_time": "20 minutes",
      "difficulty": "medium"
    }
  ]
}
```

## 🧪 Testing

### Run backend tests
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Run frontend tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 📊 Monitoring & Logging

- **CloudWatch Logs**: All Lambda function logs
- **X-Ray**: Distributed tracing (optional)
- **CloudWatch Metrics**: API Gateway, Lambda, DynamoDB metrics
- **Alarms**: Set up for error rates, latency, etc.

## 🔒 Security Best Practices

1. **Authentication**: JWT tokens with expiration
2. **Password Security**: Bcrypt hashing
3. **API Security**: CORS configuration, rate limiting
4. **Data Encryption**: At rest (S3, DynamoDB) and in transit (HTTPS)
5. **IAM**: Least privilege access for Lambda functions
6. **Secrets Management**: Use AWS Secrets Manager for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- OpenAI for AI-powered recommendations
- AWS for cloud infrastructure
- React and TypeScript communities

## 📞 Support

For support, email support@dailybread.com or open an issue in the repository.

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Integration with wearable devices
- [ ] Community forum
- [ ] Gamification features
- [ ] Multi-language support
- [ ] Nutrition tracking dashboard
- [ ] Meal planning calendar
- [ ] Social sharing features
- [ ] Admin panel for content management
- [ ] Advanced analytics

## 💡 Future Enhancements

- **Machine Learning**: Improve recommendations with user feedback
- **Real-time Chat**: Nutritionist consultation
- **Payment Integration**: Stripe for meal orders
- **Inventory Management**: For meal delivery service
- **Reviews & Ratings**: User feedback system
- **Meal Prep Videos**: Integration with video content
