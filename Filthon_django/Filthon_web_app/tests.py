import json

from django.test import TestCase


# Create your tests here.


class Test(TestCase):
    def testJson(self):
        a = {
            "username": "",
            "password": "world!"
        }

        j_data = json.dumps(a)
        print(j_data)
        from Filthon_web_app.forms import JsonForm
        from django.forms import CharField

        class TestForm(JsonForm):
            username = CharField(max_length=32)
            password = CharField(max_length=12)

        form = TestForm.from_json(j_data)
        print(form.data["username"])
        print(form.is_valid())
