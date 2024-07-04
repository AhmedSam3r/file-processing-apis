from flask import Blueprint
from project.settings import UPLOAD_FOLDER, ROOT_PATH

"""
TODO later add swager for api docuemntation
"""
file_bp = Blueprint('files', __name__, static_folder=UPLOAD_FOLDER,
                    root_path=ROOT_PATH)
