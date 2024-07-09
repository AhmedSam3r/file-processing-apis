from flask import abort, jsonify, request
from project.files import file_bp
from werkzeug.utils import secure_filename
from project.files.utils import (
    upload_file,
    valid_blob_size,
    get_random_line,
    strtobool,
    get_most_longest_x_lines,
    allowed_file,
    generate_uuid_v1,
)
from project.files.models import (
    File,
    FileMetadata
)
from project import db
from project.files.error_handler import handle_error
from project.files.tasks import process_file_metadata


@file_bp.before_app_request
def before_request():
    # return only in case of something went wrong
    print("hello from before_request")
    print('Accept', request.headers.get('Accept'))
    print('Content-Type', request.headers.get('Content-Type'))
    print('Content-Length', request.headers.get('Content-Length'))
    if request.headers.get('Accept') not in ['application/*', 'application/json', 'application/xml', 'text/plain']:
        abort(415, "Unsupported Encoding in Accept header: please ensure file format with: 'application/json , 'application/xml', 'text/plain` or `application/*")


@file_bp.get('/')
def home():
    try:
        return "<p>Hello, from files route!</p>"
    except Exception as ex:
        abort(404, ex)


@file_bp.post('/upload/')
def upload():
    try:
        blob = request.files.get('blob')
        if not blob:
            abort(400, "blob isnot found")
        valid_size, file_size = valid_blob_size(blob)
        if not valid_size:
            abort(400, "blob size exceeded max limit")
        is_allowed_file, file_ext = allowed_file(blob.filename)
        if not is_allowed_file:
            abort(400, "FIle Extension isn't allowed")

        alias = f"{generate_uuid_v1()}.{file_ext}"
        file_name = secure_filename(blob.filename)
        is_saved, file_path = upload_file(blob, alias)
        if not is_saved:
            abort(500, "failed while saving the file")

        process_file_metadata.delay(
            file_name=file_name,
            alias=alias,
            file_path=file_path,
            file_size=file_size,
        )

        return jsonify({'success': True, 'data': {'msg': 'file is being processed', 'alias': alias}}), 201
    except Exception as ex:
        handle_error(ex)


@file_bp.get('/random-line/')
def retrieve_random_line():
    try:
        id = request.args.get('id')
        reverse = strtobool(request.args.get('reverse', 'False'))
        file = db.session.query(File).filter(File.id == id).first()
        if not file:
            file = File.query.order_by(File.id.desc()).first()

        # If no files exist
        if not file:
            abort(404, "No file is found")
        line_object = get_random_line(file.alias, file.number_of_lines,
                                      reverse=reverse)
        return jsonify({'success': True, "data": line_object}), 200
    except Exception as ex:
        handle_error(ex)


@file_bp.get('/longest-<lines_count>-lines/')
def get_longest_x_lines(lines_count: str):
    try:
        id = request.args.get('id')
        if not id.isdigit() or not lines_count.isdigit():
            return jsonify({'success': False, "msg": "Invalid type for number of lines or id"}), 400
        id = int(id)
        lines_count = int(lines_count)
        file = db.session.query(File).filter(File.id == id).first()
        if not file:
            file = File.query.order_by(File.id.desc()).first()

        if not file:
            abort(404, "No file is found")

        if lines_count > 100 or file.number_of_lines < lines_count:
            abort(400, "You exceeded allowed number of lines")

        result = get_most_longest_x_lines(file.alias, lines_count)
        if not result:
            abort(500, "couldnot get the longest lines")

        return jsonify({'success': True, "data": result}), 200

    except Exception as ex:
        handle_error(ex)


@file_bp.get('/all-longest-100-lines/')
def get_longest_100_line():
    print("all-longest-100-lines")
    try:
        files_metadata = db.session.query(FileMetadata)\
            .order_by(FileMetadata.line_size.desc()).limit(100) or []
        data = []
        for file in files_metadata:
            data.append(file.to_dict())
        return jsonify({'success': True, "data": data}), 200
    except Exception as ex:
        handle_error(ex)
