from project.files import file_bp
import json
from werkzeug.exceptions import HTTPException
from flask import abort
from typing import Union


@file_bp.errorhandler(400)
@file_bp.errorhandler(404)
@file_bp.errorhandler(405)
@file_bp.errorhandler(500)
def _handle_api_error(err):
    response = err.get_response()
    response.data = json.dumps({"success": False, "Message": err.description})
    return response


def handle_error(exception: Union[HTTPException, Exception]):
    '''
    this method differentiate between werkzeug HTTP exceptions & regular Exceptions
    it handles both cases
    '''
    print("EXC ==>", exception)
    print(exception.__traceback__.tb_lineno)
    if isinstance(exception, HTTPException):
        abort(exception.code, exception.description)
    else:
        abort(500, "something went wrong while processing")
