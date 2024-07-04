from flask import jsonify
from project import app


# not working check it later
@app.errorhandler(404)
@app.errorhandler(405)
def _handle_app_api_error(ex):
    print("_handle_app_api_error")
    return jsonify(error=str(ex)), ex.code
