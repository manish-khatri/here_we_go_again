class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATION = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3" 
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'swaadanusar'
    SECRET_KEY = "mypasswordkey"

    WTF_CSRF_ENABLED = False #kind of authentication

    # Celery/Redis config
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    # Redis Cache config
    REDIS_URL = 'redis://localhost:6379/1'  # Different DB for cache
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default cache

