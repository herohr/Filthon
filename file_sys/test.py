import unittest
from file_sys import File, BaseFile, Directory


class Test(unittest.TestCase):
    def test_file_open(self):
        filepath = "/Users/herohr/PycharmProjects/Filthon/file_sys/jesus.txt"
        file = File(filepath)
        with file.open("w") as f:
            f.write("Hello world!")

        with file.open("r") as f:
            data = f.read()
            print(data)

    def test_file(self):
        filepath = "/Users/herohr/PycharmProjects/Filthon/file_sys/jesus.txt"
        file = File(filepath)

        print(file.calc_md5())

        print(file.url)

    def test_Dir(self):
        a = Directory("/Users/herohr/PycharmProjects/Filthon/file_sys/")
        print(a.path)

    def test_dir_walk(self):
        a = Directory("/Users/herohr/PycharmProjects/Filthon")
        print(a.subs_files)
        print(a.subs_dirs)
        print(a.subs_dict)