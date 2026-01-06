/**
 * Dashboard Page Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8">Welcome back, {user?.name}!</h1>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <StatCard title="Today's Calories" value="0 / 2000" color="blue" />
          <StatCard title="Protein" value="0g / 150g" color="green" />
          <StatCard title="Active Days" value="0" color="purple" />
          <StatCard title="Meals Ordered" value="0" color="orange" />
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <ActionCard
            title="Get Meal Recommendations"
            description="Get AI-powered meal suggestions based on your profile"
            link="/meal-recommendations"
            icon="🍽️"
          />
          <ActionCard
            title="Browse Recipes"
            description="Explore our library of healthy recipes"
            link="/recipes"
            icon="📚"
          />
          <ActionCard
            title="Update Profile"
            description="Keep your fitness goals and preferences up to date"
            link="/profile"
            icon="👤"
          />
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
          <p className="text-gray-600">No recent activity yet. Start by getting meal recommendations!</p>
        </div>
      </div>
    </div>
  );
};

const StatCard: React.FC<{ title: string; value: string; color: string }> = ({ title, value, color }) => {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className={`w-12 h-12 ${colorClasses[color as keyof typeof colorClasses]} rounded-lg mb-4`}></div>
      <h3 className="text-gray-600 text-sm mb-1">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
};

const ActionCard: React.FC<{ title: string; description: string; link: string; icon: string }> = ({
  title,
  description,
  link,
  icon,
}) => (
  <Link to={link} className="block bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </Link>
);

export default DashboardPage;
