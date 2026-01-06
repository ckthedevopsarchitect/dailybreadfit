/**
 * Footer Component
 */
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">Daily Bread</h3>
            <p className="text-gray-400">
              Your personal nutrition companion for a healthier lifestyle.
            </p>
          </div>
          <div>
            <h4 className="font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <a href="/about" className="text-gray-400 hover:text-white transition">
                  About Us
                </a>
              </li>
              <li>
                <a href="/recipes" className="text-gray-400 hover:text-white transition">
                  Recipes
                </a>
              </li>
              <li>
                <a href="/contact" className="text-gray-400 hover:text-white transition">
                  Contact
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Support</h4>
            <ul className="space-y-2">
              <li>
                <a href="/faq" className="text-gray-400 hover:text-white transition">
                  FAQ
                </a>
              </li>
              <li>
                <a href="/privacy" className="text-gray-400 hover:text-white transition">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/terms" className="text-gray-400 hover:text-white transition">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Connect</h4>
            <ul className="space-y-2">
              <li>
                <a href="https://facebook.com" className="text-gray-400 hover:text-white transition">
                  Facebook
                </a>
              </li>
              <li>
                <a href="https://twitter.com" className="text-gray-400 hover:text-white transition">
                  Twitter
                </a>
              </li>
              <li>
                <a href="https://instagram.com" className="text-gray-400 hover:text-white transition">
                  Instagram
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Daily Bread. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
