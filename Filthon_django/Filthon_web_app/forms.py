from django.forms import Form
import json


class JsonForm(Form):
    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, bytes):
            json_data = json_data.decode()
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return cls(json_data)
