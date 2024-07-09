import os
from dotenv import load_dotenv
from os.path import join

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
dotenv_path = join(ROOT_PATH, '.env')
load_dotenv(dotenv_path)


# we must create the directory ourselves
# later make function for that
UPLOAD_FOLDER = ROOT_PATH + '/static' + '/files'
print("---ROOT_PATH---", ROOT_PATH)
print("---UPLOAD_FOLDER---", UPLOAD_FOLDER)
APP_SETTINGS = "manage.py"
ALLOWED_EXTENSIONS = ('txt', 'sh', 'env')
POSTGRES_URI = os.environ.get("POSTGRES_URI")
print("POSTGRES_URI==>", POSTGRES_URI)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
MIN_FILE_SIZE = 1

REDIS_URI = os.environ.get("REDIS_URI")
CELERY_BROKER_URL = REDIS_URI,
CELERY_RESULT_BACKEND = REDIS_URI
