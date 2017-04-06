from flask import Flask, request, session, render_template, send_from_directory, redirect, flash, url_for
from models import User, File
from ext import db, threading, hashlib, os, pymysql
from utils import file_remove
from celery import Celery
import logging
app = Flask(__name__)
from CONFIG import pymysql_config
"""
File 模型
def __init__(self, filename, user_id, file_folder='./static/uploads/', file_type=None)
"""
app.config.from_pyfile("CONFIG.py")
db.init_app(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()


# def make_celery(app):
#
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
# celery = make_celery(app)
# celery.conf.update(app.config)


@app.route('/')
def index():
    return render_template("index.html", files=File.query.order_by(db.desc(File.upload_time)).limit(10))


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file_temp = request.files["file"]
        username = session.get("username", None)
        if file_temp and username:

            file = File(filename=file_temp.filename, user_id=username)
            file_path = ''.join([app.config["UPLOAD_FOLDER"], '\\', file.file_hash, ".", file.file_type])
            file_temp.save(file_path)
            file.set_file_path(file_path)
            # threading.Thread(target=file.calc, args=(file, file_path,)).start()
            # file_md5 = hashlib.md5()
            # file.file_size = os.path.getsize(file_path)
            # with open(file_path, 'rb') as f:
            #     while True:
            #         block = f.read(1024)
            #         if not block:
            #             break
            #         file_md5.update(block)
            # file.file_md5 = file_md5.hexdigest()
            db.session.add(file)
            db.session.commit()
            # calc.delay(file.id)
            flash("上传成功！")
            return redirect(url_for("mine"))
    return render_template("upload.html")


@app.route('/file/<file_id>')
def get_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        if not file.open:
            username = session.get("username", None)
            if session.get("condition", None) and username == file.user_id:
                return send_from_directory(app.config["UPLOAD_FOLDER"],
                                           filename=file.file_path.split("\\")[-1],
                                           as_attachment=True,
                                           attachment_filename=file.filename
                                           )
            else:
                flash('这个文件不属于你喔~或者上传者并未公开')
                return redirect('/')
        else:
            return send_from_directory(app.config["UPLOAD_FOLDER"],
                                       filename=file.file_path.split("\\")[-1],
                                       as_attachment=True,
                                       attachment_filename=file.filename
                                       )


@app.route('/file/open/<file_id>')
def open_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        username = session.get("username", None)
        if session.get("condition", None) == "PASS" and username == file.user_id:
            file.open = True
            db.session.commit()
            flash("链接: /file/{}".format(file_id))
            return redirect("/user/mine")
        else:
            flash("请登录！")
            return redirect("/user/mine")


@app.route('/file/close/<file_id>')
def close_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        username = session.get("username", None)
        if session.get("condition", None) == "PASS" and username == file.user_id:
            file.open = False
            db.session.commit()
            flash("取消公开成功")
            return redirect("/user/mine")
        else:
            flash("请登录！")
            return redirect("/user/mine")


@app.route('/file/delete/<file_id>')
def delete_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        username = session.get("username", None)
        if session.get("condition", None) and username == file.user_id:
            db.session.delete(file)
            db.session.commit()
            try:
                file_remove(file.file_path) if not File.query.filter_by(file.file_path).first() else None  # 如果有其他占用则不删除文件
            except Exception:
                pass
            flash("文件已经删除")
            return redirect("/user/mine")
        else:
            flash("请登录！")
            return redirect("/user/mine")


@app.route("/user/register", methods=["POST", "GET"])
def user_register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            username.encode('ascii')
            password.encode('ascii')
        except UnicodeEncodeError:
            flash("账户密码必须是英文、数字、符号")
            return render_template("register.html")
        if User.query.filter_by(id=username).first():
            flash("用户已经存在啦！")
            return render_template("register.html")
        db.session.add(User(id=username, password=password))
        db.session.commit()
        session['username'] = username
        session['condition'] = "PASS"
        flash("注册成功: {}".format(username))
        return redirect(url_for("mine"))
    else:
        return render_template("register.html")


@app.route("/user/login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form.get('username', None)
        if username == "用户名":
            flash("请输入用户名")
            return render_template("login.html")
        user = User.query.filter_by(id=username).first()
        if not user:
            flash("用户不存在")
            return render_template("login.html")
        password = request.form.get("password", None)
        if password == user.password:
            session["condition"] = "PASS"
            session["username"] = username
            flash("登录成功")
            return redirect(url_for('mine'))
        else:
            flash("用户密码错误")
            return redirect(url_for('user_login'))
    return render_template("login.html")


@app.route('/user/mine', methods=["POST", "GET"])
def mine():
    if request.method == "POST":
        pass
    username = session.get("username", None)
    if username and session.get("condition", None) == "PASS":
        files = File.query.filter_by(user_id=username).order_by(db.desc(File.upload_time)).limit(10)
        return render_template("mine.html", files=files if files else None)
    else:
        flash('请先登录')
        return redirect(url_for('user_login'))


# @celery.task()
# def calc(file_id):
#     _db = pymysql.connect(**pymysql_config)
#     cursor = _db.cursor()
#     cursor.execute("select file_path from file where id={}".format(file_id))
#     file_path = cursor.fetchone()[0]
#     file_md5 = hashlib.md5()
#     file_size = os.path.getsize(file_path)
#     with open(file_path, 'rb') as f:
#         while True:
#             block = f.read(1024)
#             if not block:
#                 break
#             file_md5.update(block)
#     file_md5 = file_md5.hexdigest()
#     file_size = file_size
#
#     cursor.execute("select id, file_path from file where file_md5 = {}".format(repr(file_md5)))
#     file_s = cursor.fetchone()
#     if file_s:
#         file_remove(file_path)
#         _, file_path = file_s
#
#     _db.cursor().execute("update file set file_md5={}, file_size={}, file_path={} where id={}"
#                          .format(repr(file_md5), file_size, file_id, repr(file_path)))
#     _db.commit()

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
