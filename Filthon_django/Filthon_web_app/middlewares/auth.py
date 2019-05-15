from functools import wraps
from threading import Lock

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from Filthon_web_app.utils import crypto
from uuid import uuid4


"""
加密算法采用HMAC加密算法
resut = HMAC(DATA: (user_id + UUID), SALT: (SECRET_KEY)) + UUID

session设计
{ UUID: {"user_id", "other_data"}, }
"""


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


class SessionManager:
    def __init__(self):
        self.sessions

        self.user2uuidLock = Lock()

    def create_session(self, user_id):
        uuid = uuid4()
        self.user2uuid[user_id] = uuid

    def generate_token(self, user_id, uuid):
        return crypto.generate_token(user_id, uuid, secret_key=settings.SECRET_KEY)

    def check_token(self, token, user_id):
        if user_id not in  self.user2uuid:
            return False
        uuid = self.user2uuid[user_id]
        result, user_id, _uuid = crypto.parse_token(token, secret_key=settings.SECRET_KEY)
        if result is False:
            return False
        if uuid != _uuid:
            return False
        return True


class Session:
    def __init__(self, session_id, user_id,  adapter_cls=None):
        self.adapter_cls = adapter_cls or DictAdapter
        self.id = session_id
        self.user_id = user_id
        self.data = adapter_cls()

    def get_or_default(self, key, default):
        return self.data.get(key, default)

    def get(self, key):
        none = object()
        result = self.data.get(key, none)
        if result is none:
            raise ValueError("Key: {} not in session data.session_id={}".format(key, self.id))
        return result

