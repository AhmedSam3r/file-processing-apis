from project import celery, db, app
from project.files.models import File, FileMetadata
from project.files.utils import (
    count_lines_number,
    get_most_longest_x_lines
)


@celery.task
def process_file_metadata(file_name, alias, file_path, file_size):
    with app.app_context():
        print(f"file {alias} is being processed")
        new_file = File(file_name=file_name, file_path=file_path,
                        number_of_lines=count_lines_number(file_path),
                        alias=alias,
                        file_size=file_size)
        db.session.add(new_file)
        db.session.commit()
        db.session.refresh(new_file)
        longest_100_lines = get_most_longest_x_lines(new_file.alias, 100)
        files_metadata = []
        for item in longest_100_lines:
            files_metadata.append(FileMetadata(
                file_id=new_file.id,
                line_number=item.get("index"),
                line_content=item.get("content"),
                line_size=item.get("size"))
            )
        db.session.add_all(files_metadata)
        db.session.commit()
        print(f"Inserted {len(files_metadata)} files into the database.")
