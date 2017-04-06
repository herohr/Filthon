from database_connect_consts import *  # DB_URI, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
DEBUG = True
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = r"""E:\Users\HeroHR pc\PycharmProjects\Filthon\static\uploads"""
WORKING_PATH = r"""E:\Users\HeroHR pc\PycharmProjects\Filthon"""
SECRET_KEY = "FUCKYOU"
pymysql_config = {
        'host': HOSTNAME,
        'port': PORT,
        'user': USERNAME,
        'password': PASSWORD,
        'db': DATABASE
    }
