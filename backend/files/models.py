from django.core.files.base import ContentFile
from django.db import models, IntegrityError
from django.db.models import Model

from authentication.models import ToolshedUser


def hash_upload(instance, filename):
    return f"{instance.hash[:2]}/{instance.hash[2:4]}/{instance.hash[4:6]}/{instance.hash[6:]}"


class FileManager(models.Manager):
    def get_or_create(self, **kwargs):
        if 'data' in kwargs and type(kwargs['data']) == str:
            import base64
            from hashlib import sha256
            content = base64.b64decode(kwargs['data'], validate=True)
            kwargs.pop('data')
            content_hash = sha256(content).hexdigest()
            kwargs['file'] = ContentFile(content, content_hash)
            kwargs['hash'] = content_hash
        else:
            raise ValueError('data must be a base64 encoded string or file and hash must be provided')
        try:
            return self.get(hash=kwargs['hash']), False
        except self.model.DoesNotExist:
            return self.create(**kwargs), True

    def create(self, **kwargs):
        if 'data' in kwargs and type(kwargs['data']) == str:
            import base64
            from hashlib import sha256
            content = base64.b64decode(kwargs['data'], validate=True)
            kwargs.pop('data')
            content_hash = sha256(content).hexdigest()
            kwargs['file'] = ContentFile(content, content_hash)
            kwargs['hash'] = content_hash
        elif 'file' in kwargs and 'hash' in kwargs and type(kwargs['file']) == ContentFile:
            pass
        else:
            raise ValueError('data must be a base64 encoded string or file and hash must be provided')
        if not self.filter(hash=kwargs['hash']).exists():
            return super().create(**kwargs)
        else:
            raise IntegrityError('File with this hash already exists')


class File(Model):
    file = models.FileField(upload_to=hash_upload, null=False, blank=False, unique=True)
    mime_type = models.CharField(max_length=255, null=False, blank=False)
    hash = models.CharField(max_length=64, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FileManager()
