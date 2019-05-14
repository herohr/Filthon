from functools import wraps
from threading import Lock

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
"""
加密算法采用HMAC加密算法
resut = HMAC(DATA: (user_id + user_pw + UUID), SALT: (SECRET_KEY)) + UUID

session设计
{ UUID: {"user_id", "other_data"}, }
"""
#
# class Encrypt:
#     secret = settings.SECRET_KEY
#
#     def encrypt_user_id(self, ):

def auth_exempt(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        return func(*args, **kwargs)

    _inner.auth_exempt = False
    return _inner


class BaseAdapter:
    def get(self, key, default):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def set(self, key, val):
        raise NotImplementedError()


class DictAdapter(BaseAdapter):
    def __init__(self, *args, **kwargs):
        self.dict = {}
        self._lock = Lock()

    def get(self, key, default):
        with self._lock:
            return self.dict.get(key, default)

    def delete(self, key):
        with self._lock:
            if key in self.dict:
                del self.dict[key]

    def set(self, key, val):
        with self._lock:
            self.dict[key] = val


class AuthenticationMiddleware(MiddlewareMixin):
    default_adapter_cls = DictAdapter
    default_response = HttpResponse()

    def __init__(self, get_response=None, adapter_cls=None):
        super().__init__(get_response)
        self.adapter = (adapter_cls or AuthenticationMiddleware.default_adapter_cls)()

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print(request.META.get("HTTP_CONNECTION"))
        if hasattr(callback, "auth_exempt"):
            return None
        if getattr(request, "session", False):
            user_id = request.session.get("id", default=None)
        if request.META.get("HTTP_AUTHORIZATION", False):
            pass
