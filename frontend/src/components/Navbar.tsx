/**
 * Navbar Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold text-green-600">
            Daily Bread
          </Link>

          <div className="hidden md:flex space-x-6">
            <Link to="/" className="text-gray-700 hover:text-green-600 transition">
              Home
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-green-600 transition">
                  Dashboard
                </Link>
                <Link to="/meal-recommendations" className="text-gray-700 hover:text-green-600 transition">
                  Meal Recommendations
                </Link>
                <Link to="/recipes" className="text-gray-700 hover:text-green-600 transition">
                  Recipes
                </Link>
                <Link to="/profile" className="text-gray-700 hover:text-green-600 transition">
                  Profile
                </Link>
              </>
            ) : (
              <>
                <Link to="/recipes" className="text-gray-700 hover:text-green-600 transition">
                  Recipes
                </Link>
              </>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-gray-700">Welcome, {user?.name || 'User'}</span>
                <button
                  onClick={logout}
                  className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-green-600 hover:text-green-700 transition"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
