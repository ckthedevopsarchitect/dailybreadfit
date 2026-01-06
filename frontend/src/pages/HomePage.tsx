/**
 * Home Page Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            Welcome to <span className="text-green-600">Daily Bread</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Your personal nutrition companion for a healthier lifestyle. 
            Get AI-powered meal recommendations tailored to your fitness goals.
          </p>
          <div className="flex gap-4 justify-center">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition"
                >
                  Go to Dashboard
                </Link>
                <Link
                  to="/meal-recommendations"
                  className="bg-white text-green-600 border-2 border-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition"
                >
                  Get Meal Recommendations
                </Link>
              </>
            ) : (
              <>
                <Link
                  to="/register"
                  className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition"
                >
                  Get Started
                </Link>
                <Link
                  to="/login"
                  className="bg-white text-green-600 border-2 border-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-12">Why Choose Daily Bread?</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            title="AI-Powered Recommendations"
            description="Get personalized meal recommendations based on your fitness goals, dietary preferences, and body type."
            icon="🤖"
          />
          <FeatureCard
            title="Daily Tips & Recipes"
            description="Access a library of nutritious recipes and daily health tips to maintain your wellness journey."
            icon="📚"
          />
          <FeatureCard
            title="Order Healthy Meals"
            description="Order freshly prepared, nutritious meals delivered to your doorstep based on your meal plan."
            icon="🍽️"
          />
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-green-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <StepCard number="1" title="Create Profile" description="Tell us about your fitness goals and preferences" />
            <StepCard number="2" title="Get Recommendations" description="Receive AI-powered meal suggestions" />
            <StepCard number="3" title="Track Progress" description="Monitor your nutrition and fitness journey" />
            <StepCard number="4" title="Order Meals" description="Get healthy meals delivered to you" />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Start Your Health Journey Today</h2>
        <p className="text-xl text-gray-600 mb-8">
          Join thousands of users achieving their fitness goals with Daily Bread
        </p>
        {!isAuthenticated && (
          <Link
            to="/register"
            className="inline-block bg-green-600 text-white px-12 py-4 rounded-lg font-semibold text-lg hover:bg-green-700 transition"
          >
            Sign Up Now - It's Free
          </Link>
        )}
      </section>
    </div>
  );
};

const FeatureCard: React.FC<{ title: string; description: string; icon: string }> = ({
  title,
  description,
  icon,
}) => (
  <div className="bg-white p-8 rounded-lg shadow-lg text-center">
    <div className="text-6xl mb-4">{icon}</div>
    <h3 className="text-2xl font-bold mb-3">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const StepCard: React.FC<{ number: string; title: string; description: string }> = ({
  number,
  title,
  description,
}) => (
  <div className="text-center">
    <div className="bg-green-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
      {number}
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

export default HomePage;
