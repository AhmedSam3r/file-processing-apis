import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# we must create the directory ourselves
# later make function for that
UPLOAD_FOLDER = ROOT_PATH + '/static' + '/files'
print("---ROOT_PATH---", ROOT_PATH)
print("---UPLOAD_FOLDER---", UPLOAD_FOLDER)
APP_SETTINGS = "manage.py"
ALLOWED_EXTENSIONS = ('txt', 'sh', 'env')
