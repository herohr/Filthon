from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

print(settings)
file_upload_root = settings.FILE_UPLOAD_ROOT


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()


class UploadFileView(View):
    def get(self, request):
        return render(request, "upload.html")

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            with open(file_upload_root+"/"+file.name, "wb") as f:
                chunked_write(f, upload_file=file)
            return HttpResponse("Success")
        else:
            print(form.errors, form.cleaned_data)
            return HttpResponse("Faild")


def chunked_write(file, upload_file):
    for chunk in upload_file.chunks():
        file.write(chunk)
