"""
Configuration settings for Daily Bread backend
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # AWS Settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # DynamoDB Tables
    USERS_TABLE: str = os.getenv("USERS_TABLE", "dailybread-users")
    USER_PROFILES_TABLE: str = os.getenv("USER_PROFILES_TABLE", "dailybread-user-profiles")
    RECIPES_TABLE: str = os.getenv("RECIPES_TABLE", "dailybread-recipes")
    DAILY_TIPS_TABLE: str = os.getenv("DAILY_TIPS_TABLE", "dailybread-daily-tips")
    USER_FAVORITES_TABLE: str = os.getenv("USER_FAVORITES_TABLE", "dailybread-user-favorites")
    ORDERS_TABLE: str = os.getenv("ORDERS_TABLE", "dailybread-orders")
    MEAL_PLANS_TABLE: str = os.getenv("MEAL_PLANS_TABLE", "dailybread-meal-plans")
    
    # S3 Buckets
    CONTENT_BUCKET: str = os.getenv("CONTENT_BUCKET", "dailybread-content")
    USER_UPLOADS_BUCKET: str = os.getenv("USER_UPLOADS_BUCKET", "dailybread-user-uploads")
    
    # Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # OpenAI API (for AI recommendations)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Stripe (for payments)
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # API Settings
    API_VERSION: str = "v1"
    PROJECT_NAME: str = "Daily Bread API"
    
    class Config:
        case_sensitive = True


settings = Settings()
