class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATION = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3" 
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'swaadanusar'
    SECRET_KEY = "mypasswordkey"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication_token'

    WTF_CSRF_ENABLED = False #kind of authentication

