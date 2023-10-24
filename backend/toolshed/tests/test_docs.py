from django.test import Client
from authentication.tests import UserTestMixin, SignatureAuthClient, ToolshedTestCase
from backend import settings
from toolshed.tests import CategoryTestMixin, TagTestMixin, PropertyTestMixin

anonymous_client = Client()
client = SignatureAuthClient()


class OpenapiTestCase(UserTestMixin, CategoryTestMixin, TagTestMixin, PropertyTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()

    def test_docs_anonymous(self):
        response = anonymous_client.get('/docs/?format=openapi')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('swagger' in response.json())
        self.assertTrue('info' in response.json())

