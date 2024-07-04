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
    count_lines_number
)
from project.files.models import (
    File,
    FileMetadata
)
from project import db


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
        print('1')
        blob = request.files.get('blob')
        if not blob:
            return jsonify({'success': False, 'msg': "blob isnot found"}), 400
        valid_size, file_size = valid_blob_size(blob)
        if not valid_size:
            return jsonify({'success': False,
                            'msg': "blob size exceeded max limit"}), 400
        if not allowed_file(blob.filename):
            return jsonify({'success': False,
                            'msg': "not allowed file"}), 400
        print('2')
        # TODO create unique name for file
        file_name = secure_filename(blob.filename)
        is_saved, file_path = upload_file(blob, file_name)
        if not is_saved:
            return jsonify({'success': False,
                            'msg': "failed while saving"}), 400
        # TODO make that part async
        new_file = File(file_name=file_name, file_path=file_path,
                        number_of_lines=count_lines_number(file_path, file_name),
                        file_size=file_size)
        db.session.add(new_file)
        db.session.commit()
        db.session.refresh(new_file)
        # TODO move it to be async task in the background
        longest_100_lines = get_most_longest_x_lines(new_file.file_name, 100)
        files_metadata = []
        for item in longest_100_lines:
            files_metadata.append(FileMetadata(
                file_id=new_file.id,
                line_number=item.get("index"),
                line_content=item.get("content"),
                line_size=item.get("size"))
            )
        print("files_metadata ==> ", files_metadata)
        db.session.add_all(files_metadata)
        db.session.commit()
        print(f"Inserted {len(files_metadata)} files into the database.")

        return jsonify({'success': True, 'id': new_file.id}), 201
    except Exception as ex:
        print("EX ==>,", ex)
        abort(500, ex)


@file_bp.get('/random-line/')
def retrieve_random_line():
    try:
        id = request.args.get('id')
        reverse = strtobool(request.args.get('reverse', 'False'))
        if file := db.session.query(File).filter(File.id == id):
            file = file.first()
            print("FILE = ", file)
        else:
            file: File = File.query.order_by(File.id.desc()).first()

        if not file:
            return jsonify({'success': False,
                            'msg': "No file is found"}), 404
        line_object = get_random_line(file.file_name, file.number_of_lines,
                                      reverse=reverse)

        return jsonify({'success': True, "info": line_object}), 200
    except Exception as ex:
        print("ERR ==> ", ex)
        abort(500, ex)


@file_bp.get('/longest-<lines_count>-lines/')
def get_longest_x_lines(lines_count: str):
    try:
        id = request.args.get('id')
        if not id.isdigit() or not lines_count.isdigit():
            return jsonify({'success': False, "msg": "Invalid type for number of lines or id"}), 400
        id = int(id)
        lines_count = int(lines_count)
        if file := db.session.query(File).filter(File.id == id):
            file = file.first()
        else:
            file: File = File.query.order_by(File.id.desc()).first()
        if lines_count > 100 or file.number_of_lines < lines_count:
            return jsonify({'success': False, "msg": "You exceeded allowed number of lines"}), 400

        result = get_most_longest_x_lines(file.file_name, lines_count)
        if not result:
            return jsonify({'success': False, "longest_lines": None,
                            "message": "Ensure the number of lines donot exceed the file number of lines"}), 500
        return jsonify({'success': True, "longest_lines": result}), 200
    except Exception as ex:
        print("ERR ==> ", ex)
        abort(500, ex)


@file_bp.get('/all-longest-100-lines/')
def get_longest_100_line():
    print("all-longest-100-lines")
    try:
        files_metadata = db.session.query(FileMetadata)\
            .order_by(FileMetadata.line_size.desc()).limit(100)
        data = []
        for file in files_metadata:
            data.append(file.to_dict())
        return jsonify({'success': True, "data": data}), 200
    except Exception as ex:
        print("ERR ==> ", ex)
        abort(500, ex)
