import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode


def get_django_secret():
    from django.conf import settings
    secret_key = settings.SECRET_KEY
    return secret_key


def md5(key, msg):
    if isinstance(key, str):
        key = key.encode()

    if isinstance(msg, str):
        msg = msg.encode()

    obj = hmac.new(key, msg, "MD5")
    return obj.digest()


def generate_token(user_id, uuid, secret_key=None):
    if secret_key is None:
        secret_key = get_django_secret()

    message = "{}.{}".format(user_id, uuid)
    _md5 = md5(secret_key, message)
    pre = urlsafe_b64encode(_md5).decode()
    return "{}.{}.{}".format(pre, user_id, uuid)


def parse_token(token, secret_key=None):
    if secret_key is None:
        secret_key = get_django_secret()

    pre, user_id, uuid = token.split(".")
    pre = urlsafe_b64decode(pre)
    # print(pre, md5(secret_key, "{}.{}".format(user_id, uuid)))
    if pre == md5(secret_key, "{}.{}".format(user_id, uuid)):
        return True, user_id, uuid
    else:
        return False, None, None