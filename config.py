"""
This file stores all the possible configurations for the Flask app.
Changing configurations like the secret key or the database
url should be stored as environment variables and imported
using the 'os' library in Python.
"""
import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DRIVER = os.getenv('MSSQL_DRIVER', 'ODBC Driver 13 for SQL Server')
    SERVER = os.getenv('MSSQL_SERVER', 'localhost')
    PORT = os.getenv('MSSQL_PORT', 1433)
    USERNAME = os.getenv('MSSQL_USERNAME', 'sa')
    PASSWORD = os.getenv('MSSQL_PASSWORD', 'YourStrong!Passw0rd')
    COLLECT_METRICS_INTERVAL_SEC = int(
        os.getenv('COLLECT_METRICS_INTERVAL_SEC', 120))
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
