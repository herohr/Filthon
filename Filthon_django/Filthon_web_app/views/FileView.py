from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from . import authorized
from Filthon_web_app.models import LocalFile
from Filthon_web_app.middlewares.auth import auth_exempt

file_upload_root = settings.FILE_UPLOAD_ROOT


class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=64)
    file = forms.FileField()


class UploadFileView(View):
    @authorized
    def get(self, request):
        return render(request, "upload.html")

    @authorized
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = file_upload_root + "/" + file.name
            with open(file_path, "wb") as f:
                size = chunked_write(f, upload_file=file)

            local_file = LocalFile(filename=file.name, file_size=size, url="file://{}".format(file_path),
                                   user_id=request.user)
            local_file.save()
            return HttpResponse("Success")
        else:
            print(form.errors, form.cleaned_data)
            return HttpResponse("Failed")

    @auth_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileView, self).dispatch(request, *args, **kwargs)


def chunked_write(file, upload_file):
    size = 0
    for chunk in upload_file.chunks():
        file.write(chunk)
        size += len(chunk)
    return size
