"""
本模块提供文件系统的操作

对文件系统：
    1.将文件以字典的形式组织
    2.获取文件元数据

对文件：
    1.提供读写操作
    2.提供流操作
"""
import os
import hashlib

p = "/Users/herohr/PycharmProjects/Filthon/file_sys/__init__.py"


class BaseFile:
    def __init__(self, path):
        # self.name = name
        self.path = self._path_preprocess(path)

    @staticmethod
    def get_name_by_path(path):
        if not path:
            raise ValueError("Path name must be give out.")

        name = os.path.basename(path)
        if not name:
            if path[-1] == "/":
                name = os.path.basename(path[:-1])
        return name

    @staticmethod
    def _path_preprocess(path):
        if not os.path.exists(path):
            raise OSError("Path {} dose not exist.".format(path))

        # path = os.path.expandvars(path)  # 去除$环境变量
        path = os.path.realpath(path)  # 绝对路径变为相对路径
        path = os.path.normpath(path)  # 将路径标准化

        return path

    @staticmethod
    def get_path_type(path):
        if os.path.isfile(path):
            return File
        if os.path.isdir(path):
            return Directory

        raise ValueError("Path is neither a file nor a dir...")


# print(BaseFile.get_name_by_path("/Users/herohr/PycharmProjects/Filthon/file_sys/.sf/"))


class File(BaseFile):
    def __init__(self, path):
        super().__init__(path)
        self.name = BaseFile.get_name_by_path(path)

    def open(self, *args, **kwargs):
        return open(self.path, *args, **kwargs)

    def calc_md5(self):
        md5_ins = hashlib.md5()
        with self.open("rb") as flow:
            data = b"1"
            while data:
                data = flow.read(8096)
                md5_ins.update(data)

        return md5_ins.hexdigest()

    @property
    def url(self):
        return "file://{}".format(self.path)

    def __repr__(self):
        return "<File object: {}>".format(self.name)


def lazy_proxy(ins_method):
    def inner(func):
        def _inner(self, *args, **kwargs):
            ins_method(self, *args, **kwargs)
            return func(self, *args, **kwargs)

        return _inner

    return inner


class Directory(BaseFile):
    def __init__(self, path):
        super().__init__(path)
        self.name = BaseFile.get_name_by_path(path)
        self._subs_dict = None
        self._subs_files = None
        self._subs_dir = None

    # def walk(self, depth=1):
    #     for names in os.listdir(self.path):

    def _subs_init(self):
        if self._subs_dict is None:
            if self._subs_dict is None:
                self._subs_dict = {}
                self._subs_files = []
                self._subs_dir = []
                for name in os.listdir(self.path):
                    path = "{}/{}".format(self.path, name)
                    cls = BaseFile.get_path_type(path)
                    ins = cls(path)
                    self._subs_dict[ins.name] = ins

                    if isinstance(ins, File):
                        self._subs_files.append(ins)
                    else:
                        self._subs_dir.append(ins)

    @property
    @lazy_proxy(_subs_init)
    def subs_dict(self):
        return self._subs_dict.items()

    @property
    @lazy_proxy(_subs_init)
    def subs_files(self):
        return self._subs_files

    @property
    @lazy_proxy(_subs_init)
    def subs_dirs(self):
        return self._subs_dir

    def __repr__(self):
        return "<Directory object: {}>".format(self.name)
