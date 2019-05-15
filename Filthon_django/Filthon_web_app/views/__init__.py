import json

from django.http import HttpResponse
from django.views import View
from Filthon_web_app.models import User
from Filthon_web_app.middlewares.auth import auth_exempt


class ApiView(View):
    def setup(self, request, *args, **kwargs):
        json_data = request.body
        val = json.loads(json_data)
        setattr(request, "json", val)
        super(ApiView, self).setup(request, *args, **kwargs)


class AuthExemptView(View):
    @auth_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AuthExemptView, self).dispatch(request, *args, **kwargs)


def authorized(func):
    def inner(self, request, *args, **kwargs):
        user_id = request.session.get("id", default=None)
        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponse("User auth failed!")

            setattr(request, "user", user)
            return func(self, request, *args, **kwargs)
        else:
            return HttpResponse("User auth failed!")
    return inner
