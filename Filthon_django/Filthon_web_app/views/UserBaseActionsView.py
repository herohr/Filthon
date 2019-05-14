from django.views import View
from django.contrib.auth.models import UserManager
from django.shortcuts import render
from django.http import HttpResponse
from django.forms import Form, CharField
from Filthon_web_app.forms import JsonForm
from Filthon_web_app.models import User
from . import ApiView


user_manager = UserManager()


def get_user_by_name(username, default=None):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return default


class UserLoginForm(Form):
    username = CharField(max_length=150, label="用户名")
    password = CharField(max_length=128, label="密码")


class UserRegisterForm(UserLoginForm):
    pass


class UserRegisterView(View):
    def get(self, request):
        return render(request, "register.html", {"register_form": UserRegisterForm()})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            user_e = get_user_by_name(form.data["username"])
            print(form.data["password"])
            if user_e is None:
                User.objects.create_user(username=form.data["username"], password=form.data["password"])
                return HttpResponse("Register Success, {}".format(form.data["username"]))
            else:
                return HttpResponse("Username exist.")

        else:
            return HttpResponse("Form failed")


class UserLoginView(View):
    def get(self, request):
        return render(request, "login.html", {"login_form": UserLoginForm()})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = get_user_by_name(username=form.data['username'])
            if user is not None:
                if user.check_password(form.data["password"]):
                    request.session["id"] = user.id
                    return HttpResponse("login Success, {}".format(form.data["username"]))
                else:
                    return HttpResponse("Login failed, password wrong.")
            else:
                return HttpResponse()

        else:
            return HttpResponse("Form failed")
