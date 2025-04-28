import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App version
APP_VERSION = "2.1.0"

# Environment configurations
class Config:
    """Base config for NutriCalc AI application"""
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv("MONGO_URI")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    APP_VERSION = APP_VERSION
    
class DevelopmentConfig(Config):
    """Development environment config"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing environment config"""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Production environment config"""
    # Production-specific settings
    pass

# Define the active configuration based on environment variable
ENV = os.getenv("FLASK_ENV", "development")
if ENV == "production":
    app_config = ProductionConfig
elif ENV == "testing":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig
