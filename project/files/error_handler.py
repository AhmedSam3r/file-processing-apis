from flask import jsonify
from project.files import file_bp


# not working check it later
@file_bp.errorhandler(404)
@file_bp.errorhandler(405)
def _handle_api_error(ex):
    print("_handle_api_error")
    return jsonify(error=str(ex)), ex.code
