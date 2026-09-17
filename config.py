import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent

    STATIC_FOLDER = BASE_DIR / 'static'
    FILES_FOLDER = STATIC_FOLDER / 'files'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'srinurao1902@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'srinurao1902@gmail.com')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'srininvast20@gmail.com')
    ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP', '8341492762')
    WHATSAPP_COUNTRY_CODE = os.environ.get('WHATSAPP_COUNTRY_CODE', '91')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '918341492762')

    _is_vercel = os.environ.get('VERCEL', '') == '1'

    if _is_vercel:
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            'sqlite:////tmp/portfolio.db'
        )
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            'sqlite:///' + str(BASE_DIR / 'instance' / 'portfolio.db')
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() in ['true', 'on', '1']
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    DEBUG = False
    TESTING = False
    SITE_URL = os.environ.get('SITE_URL', 'https://srinivas-profile.vercel.app')

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        import logging
        app.logger.setLevel(logging.INFO)
        app.logger.info('Portfolio startup')

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key-for-testing')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
