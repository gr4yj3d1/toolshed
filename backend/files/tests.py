from django.core.files.base import ContentFile
from django.core.files.storage import DefaultStorage
from django.db import IntegrityError, transaction
from django.test import Client
from authentication.tests import SignatureAuthClient, ToolshedTestCase, UserTestMixin
from nacl.hash import sha256
from nacl.encoding import HexEncoder
import base64

from files.models import File

anonymous_client = Client()
client = SignatureAuthClient()


def rmdir(storage, path):
    dirs, files = storage.listdir(path)
    for file in files:
        storage.delete(path + file)
    for dir in dirs:
        rmdir(storage, path + dir + "/")
    storage.delete(path)


def countdir(storage, path):
    dirs, files = storage.listdir(path)
    count = len(files)
    for dir in dirs:
        count += countdir(storage, path + dir + "/")
    return count


class FilesTestMixin:
    def prepare_files(self):
        rmdir(DefaultStorage(), '')
        self.f['test_content1'] = b'testcontent1'
        self.f['hash1'] = sha256(self.f['test_content1'], encoder=HexEncoder).decode('utf-8')
        self.f['encoded_content1'] = base64.b64encode(self.f['test_content1']).decode('utf-8')
        self.f['test_file1'] = File.objects.create(mime_type='text/plain', data=self.f['encoded_content1'])
        self.f['test_content2'] = b'testcontent2'
        self.f['hash2'] = sha256(self.f['test_content2'], encoder=HexEncoder).decode('utf-8')
        self.f['encoded_content2'] = base64.b64encode(self.f['test_content2']).decode('utf-8')
        self.f['test_file2'] = File.objects.create(mime_type='text/plain', data=self.f['encoded_content2'])
        self.f['test_content3'] = b'testcontent3'
        self.f['hash3'] = sha256(self.f['test_content3'], encoder=HexEncoder).decode('utf-8')
        self.f['encoded_content3'] = base64.b64encode(self.f['test_content3']).decode('utf-8')
        self.f['test_file3'] = File.objects.create(mime_type='text/plain', data=self.f['encoded_content3'])
        self.f['test_content4'] = b'testcontent4'
        self.f['hash4'] = sha256(self.f['test_content4'], encoder=HexEncoder).decode('utf-8')
        self.f['encoded_content4'] = base64.b64encode(self.f['test_content4']).decode('utf-8')


class FilesTestCase(FilesTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_files()

    def test_file_list(self):
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(countdir(DefaultStorage(), ''), 3)

    def test_file_upload(self):
        File.objects.create(mime_type='text/plain', data=self.f['encoded_content4'])
        self.assertEqual(File.objects.count(), 4)
        self.assertEqual(countdir(DefaultStorage(), ''), 4)
        self.assertEqual(File.objects.get(id=4).file.read(), self.f['test_content4'])
        self.assertEqual(File.objects.get(id=4).file.name,
                         f"{self.f['hash4'][:2]}/{self.f['hash4'][2:4]}/{self.f['hash4'][4:6]}/{self.f['hash4'][6:]}")

    def test_file_upload_fail(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                File.objects.create(file=ContentFile(self.f['test_content4']), mime_type='text/plain')
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(countdir(DefaultStorage(), ''), 3)

    def test_file_upload_duplicate(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                File.objects.create(mime_type='text/plain', data=self.f['encoded_content3'])
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(countdir(DefaultStorage(), ''), 3)

    def test_file_upload_get_or_create(self):
        file, created = File.objects.get_or_create(data=self.f['encoded_content3'])
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(countdir(DefaultStorage(), ''), 3)
        self.assertFalse(created)
        self.assertEqual(file.file.read(), self.f['test_content3'])
        self.assertEqual(file.file.name,
                         f"{self.f['hash3'][:2]}/{self.f['hash3'][2:4]}/{self.f['hash3'][4:6]}/{self.f['hash3'][6:]}")
        file, created = File.objects.get_or_create(data=self.f['encoded_content4'])
        self.assertEqual(File.objects.count(), 4)
        self.assertEqual(countdir(DefaultStorage(), ''), 4)
        self.assertTrue(created)
        self.assertEqual(file.file.read(), self.f['test_content4'])
        self.assertEqual(file.file.name,
                         f"{self.f['hash4'][:2]}/{self.f['hash4'][2:4]}/{self.f['hash4'][4:6]}/{self.f['hash4'][6:]}")

    def test_file_upload_get_or_create_fail(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                File.objects.get_or_create(hash=self.f['hash3'])
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(countdir(DefaultStorage(), ''), 3)


class MediaUrlTestCase(FilesTestMixin, UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_files()
        self.prepare_users()

    def test_file_url(self):
        reply = client.get(
            f"/media/{self.f['hash1'][:2]}/{self.f['hash1'][2:4]}/{self.f['hash1'][4:6]}/{self.f['hash1'][6:]}",
            self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.headers['X-Accel-Redirect'],
                         f"/redirect_media/{self.f['hash1'][:2]}/{self.f['hash1'][2:4]}/{self.f['hash1'][4:6]}/{self.f['hash1'][6:]}")
        self.assertEqual(reply.content_type, self.f['test_file1'].mime_type)
        reply = client.get(
            f"/media/{self.f['hash2'][:2]}/{self.f['hash2'][2:4]}/{self.f['hash2'][4:6]}/{self.f['hash2'][6:]}",
            self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.headers['X-Accel-Redirect'],
                         f"/redirect_media/{self.f['hash2'][:2]}/{self.f['hash2'][2:4]}/{self.f['hash2'][4:6]}/{self.f['hash2'][6:]}")
        self.assertEqual(reply.content_type, self.f['test_file2'].mime_type)

    def test_file_url_fail(self):
        reply = client.get('/media/{}/'.format('nonexistent'), self.f['local_user1'])
        self.assertEqual(reply.status_code, 404)
        self.assertTrue('X-Accel-Redirect' not in reply.headers)


