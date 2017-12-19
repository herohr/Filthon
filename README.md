# Filthon -- fileupload with python

## 基于Flask的文件托管

### Installation

```
pip3 install flask, pymysql, flask-sqlalchemy
```

### 上传
http://localhost:5000默认使用flask的werkzug wsgi服务器，部署时建议使用gunicorn + nginx代理。

文件储存于/static文件夹内
