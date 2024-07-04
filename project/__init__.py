from flask import Flask
from project.files import file_bp
from project.settings import UPLOAD_FOLDER
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
print("---------- init.py file ----------")

# postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/file_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure app to save files there
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit


# Invoking routes to be identified in the flask routing system
from project.routes import *
from project.files.routes import *

# Import models
from project.files.models import File

app.config['SQLALCHEMY_MIGRATE_REPO'] = 'project/migrations'
migrate = Migrate(app, db)

# Avoid error of AssertionError: The setup method 'before_app_request' can no longer be called on the blueprint 'files'. It has already been registered at least once, any changes will not be applied consistently
# Registering blueprints
app.register_blueprint(file_bp, url_prefix='/files')
