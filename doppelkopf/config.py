import os
import json

with open('config.json') as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URL')
    DELETE_DAYS = config.get('DELETE_DAYS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
