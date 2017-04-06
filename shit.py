import pymysql
import CONFIG
import hashlib
import os
from utils import file_remove
file_id = 42
_db = pymysql.connect(**CONFIG.pymysql_config)
cursor = _db.cursor()
cursor.execute("select file_path from file where id={}".format(file_id))
file_path = cursor.fetchone()[0]
file_md5 = hashlib.md5()
file_size = os.path.getsize(file_path)
with open(file_path, 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        file_md5.update(block)
file_md5 = file_md5.hexdigest()
file_size = file_size

cursor.execute("select id, file_path from file where file_md5 = {}".format(repr(file_md5)))  # 查找有没有已经存在的文件
file_s = cursor.fetchone()
if file_s:
    file_remove(file_path)  # 删除上传过的那个文件
    _, file_path = file_s

_db.cursor().execute("update file set file_md5={}, file_size={}, file_path={} where id={}"
                     .format(repr(file_md5), file_size, file_id, repr(file_path)))
_db.commit()