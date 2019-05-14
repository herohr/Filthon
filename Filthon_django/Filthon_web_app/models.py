from django.contrib.auth.models import AbstractUser, Group as _Group
from django.db.models import *

__all__ = ["User", "File", "LocalFile", "RemoteFile"]


# Create your models here.
class User(AbstractUser):
    pass


class File(Model):
    id = AutoField(primary_key=True)
    filename = CharField(max_length=256)

    file_size = PositiveIntegerField()

    url = URLField()

    user_id = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        abstract = True


class LocalFile(File):
    path = CharField(max_length=1024)

    class Meta:
        abstract = False


class RemoteFile(File):
    region = CharField(max_length=256, verbose_name="云储存地域、服务商")

    class Meta:
        abstract = False
