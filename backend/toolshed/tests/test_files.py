from django.test import Client
from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from files.tests import FilesTestMixin
from toolshed.models import File

from toolshed.tests import InventoryTestMixin

anonymous_client = Client()
client = SignatureAuthClient()


class FileApiTestCase(UserTestMixin, FilesTestMixin, InventoryTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_files()
        self.prepare_categories()
        self.prepare_tags()
        self.prepare_properties()
        self.prepare_inventory()
        self.f['item1'].files.add(self.f['test_file1'])
        self.f['item1'].files.add(self.f['test_file2'])
        self.f['item2'].files.add(self.f['test_file1'])

    def test_files_anonymous(self):
        response = anonymous_client.get(f"/api/item_files/{self.f['item1'].id}/")
        self.assertEqual(response.status_code, 403)

    def test_list_all_files(self):
        response = client.get(f"/api/files/", self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['mime_type'], 'text/plain')
        self.assertEqual(response.json()[0]['name'],
                         f"/media/{self.f['hash1'][:2]}/{self.f['hash1'][2:4]}/{self.f['hash1'][4:6]}/{self.f['hash1'][6:]}")
        self.assertEqual(response.json()[1]['mime_type'], 'text/plain')
        self.assertEqual(response.json()[1]['name'],
                         f"/media/{self.f['hash2'][:2]}/{self.f['hash2'][2:4]}/{self.f['hash2'][4:6]}/{self.f['hash2'][6:]}")

    def test_files(self):
        response = client.get(f"/api/item_files/{self.f['item1'].id}/", self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['mime_type'], 'text/plain')
        self.assertEqual(response.json()[0]['name'],
                         f"/media/{self.f['hash1'][:2]}/{self.f['hash1'][2:4]}/{self.f['hash1'][4:6]}/{self.f['hash1'][6:]}")
        self.assertEqual(response.json()[1]['mime_type'], 'text/plain')
        self.assertEqual(response.json()[1]['name'],
                         f"/media/{self.f['hash2'][:2]}/{self.f['hash2'][2:4]}/{self.f['hash2'][4:6]}/{self.f['hash2'][6:]}")

    def test_files_not_found(self):
        response = client.get(f"/api/item_files/99999/", self.f['local_user1'])
        self.assertEqual(response.status_code, 404)

    def test_post_file(self):
        response = client.post(f"/api/item_files/{self.f['item1'].id}/", self.f['local_user1'],
                               {'data': self.f['encoded_content4'], 'mime_type': 'text/plain'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(File.objects.count(), 4)
        self.assertEqual(File.objects.last().mime_type, 'text/plain')
        self.assertEqual(File.objects.last().file.read(), self.f['test_content4'])
        self.assertEqual(File.objects.last().file.size, len(self.f['test_content4']))
        self.assertEqual(File.objects.last().file.name,
                         f"{self.f['hash4'][:2]}/{self.f['hash4'][2:4]}/{self.f['hash4'][4:6]}/{self.f['hash4'][6:]}")

    def test_post_file_duplicate(self):
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 2)
        response = client.post(f"/api/item_files/{self.f['item1'].id}/", self.f['local_user1'],
                               {'data': self.f['encoded_content3'], 'mime_type': 'text/plain'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 3)
        self.assertEqual(self.f['item1'].files.last().file.read(), self.f['test_content3'])
        self.assertEqual(self.f['item1'].files.last().file.size, len(self.f['test_content3']))
        self.assertEqual(self.f['item1'].files.last().file.name,
                         f"{self.f['hash3'][:2]}/{self.f['hash3'][2:4]}/{self.f['hash3'][4:6]}/{self.f['hash3'][6:]}")

    def test_post_file_invalid(self):
        response = client.post(f"/api/item_files/{self.f['item1'].id}/", self.f['local_user1'],
                               {'data': self.f['encoded_content4']})
        self.assertEqual(response.status_code, 400)

    def test_post_file_not_found_item(self):
        response = client.post(f"/api/item_files/99999/", self.f['local_user1'],
                               {'data': self.f['encoded_content3'], 'mime_type': 'text/plain'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(File.objects.count(), 3)

    def test_post_file_not_authenticated(self):
        response = anonymous_client.post(f"/api/item_files/{self.f['item1'].id}/",
                                         {'data': self.f['encoded_content3'], 'mime_type': 'text/plain'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(File.objects.count(), 3)

    def test_post_file_not_authorized(self):
        response = client.post(f"/api/item_files/{self.f['item1'].id}/", self.f['local_user2'],
                               {'data': self.f['encoded_content3'], 'mime_type': 'text/plain'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(File.objects.count(), 3)

    def test_delete_file(self):
        response = client.delete(f"/api/item_files/{self.f['item1'].id}/{self.f['test_file1'].id}/",
                                 self.f['local_user1'])
        self.assertEqual(response.status_code, 204)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 1)

    def test_delete_file_last_use(self):
        response = client.delete(f"/api/item_files/{self.f['item1'].id}/{self.f['test_file2'].id}/",
                                 self.f['local_user1'])
        self.assertEqual(response.status_code, 204)
        self.assertEqual(File.objects.count(), 2)
        self.assertEqual(self.f['item1'].files.count(), 1)

    def test_delete_file_not_found(self):
        response = client.delete(f"/api/item_files/{self.f['item1'].id}/99999/", self.f['local_user1'])
        self.assertEqual(response.status_code, 404)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 2)

    def test_delete_file_not_found_item(self):
        response = client.delete(f"/api/item_files/99999/{self.f['test_file1'].id}/", self.f['local_user1'])
        self.assertEqual(response.status_code, 404)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 2)

    def test_delete_file_not_owner(self):
        response = client.delete(f"/api/item_files/{self.f['item1'].id}/{self.f['test_file1'].id}/",
                                 self.f['local_user2'])
        self.assertEqual(response.status_code, 404)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 2)

    def test_delete_file_anonymous(self):
        response = anonymous_client.delete(f"/api/item_files/{self.f['item1'].id}/{self.f['test_file1'].id}/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(File.objects.count(), 3)
        self.assertEqual(self.f['item1'].files.count(), 2)
