import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hospeed_user:password@localhost/hospeed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
