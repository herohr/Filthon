from ext import db, datetime, hashlib


class File(db.Model):
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(30), nullable=False)
    open = db.Column(db.Boolean, default=False)
    file_hash = db.Column(db.String(32), nullable=False)
    file_type = db.Column(db.String(10), default="file")
    file_size = db.Column(db.Integer, nullable=True)
    file_md5 = db.Column(db.String(32), nullable=True)
    upload_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    file_path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('user.id'))

    def __init__(self, filename, user_id):
        self.filename = filename.encode('utf-8')
        self.user_id = user_id
        self.file_type = File._get_type(filename)
        self.file_hash = File._filename_hash(filename)
        self.file_path = ''

    def set_file_path(self, path):
        self.file_path = path

    @staticmethod
    def _get_type(filename):
        typ = filename.split('.')[-1]
        return typ if typ != filename else "file"

    @staticmethod
    def _filename_hash(filename):
        """用当前时间来哈希文件,用于储存文件"""
        time = str(datetime.datetime.now())
        filename_hash = hashlib.md5()
        filename_hash.update((filename+time).encode("utf-8"))
        return filename_hash.hexdigest()

    # @staticmethod
    # def calc(file, file_path):
    #     # file = File.queue.get()
    #     with app.app_context():
    #         file_md5 = hashlib.md5()
    #         file_size = os.path.getsize(file_path)
    #         with open(file_path, 'rb') as f:
    #             while True:
    #                 block = f.read(1024)
    #                 if not block:
    #                     break
    #                 file_md5.update(block)
    #         file.file_md5 = file_md5.hexdigest()
    #         file.file_size = file_size
    #         # db.session.flush()
    #         db.session.commit()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(16), nullable=False)

    files = db.relationship("File", backref="user")

    def __init__(self, id, password):
        self.id = id
        self.password = password

