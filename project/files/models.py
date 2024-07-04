from project import db


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    number_of_lines = db.Column(db.Integer, nullable=False)
    file_size = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<File {self.file_name}>"


class FileMetadata(db.Model):
    __tablename__ = 'file_metadata'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey(File.id, ondelete='CASCADE'))
    line_number = db.Column(db.Integer, nullable=False)
    line_content = db.Column(db.Text, nullable=False)
    line_size = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'index': self.line_number,
            'size': self.line_size,
            'content': self.line_content,

        }
