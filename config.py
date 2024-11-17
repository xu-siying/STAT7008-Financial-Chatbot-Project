SECRET_KEY = "your_secret_key"
SQLALCHEMY_DATABASE_URI = "sqlite:///chatbot.db"
SESSION_TYPE = "redis"
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True
SESSION_KEY_PREFIX = "chatbot:"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
