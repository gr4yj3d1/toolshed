from django.test import Client
from authentication.tests import UserTestMixin, SignatureAuthClient, ToolshedTestCase
from backend import settings
from toolshed.tests import CategoryTestMixin, TagTestMixin, PropertyTestMixin

anonymous_client = Client()
client = SignatureAuthClient()


class CombinedApiTestCase(UserTestMixin, CategoryTestMixin, TagTestMixin, PropertyTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()
        self.prepare_properties()

    def test_version_anonymous(self):
        response = anonymous_client.get('/api/version/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'version': settings.TOOLSHED_VERSION})

    def test_version_authenticated(self):
        response = client.get('/api/version/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'version': settings.TOOLSHED_VERSION})

    def test_domains_anonymous(self):
        response = anonymous_client.get('/api/domains/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['example.com'])

    def test_domains_authenticated(self):
        response = client.get('/api/domains/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['example.com'])

    def test_policy_api_anonymous(self):
        response = anonymous_client.get('/api/availability_policies/')
        self.assertEqual(response.status_code, 403)

    def test_policy_api(self):
        response = client.get('/api/availability_policies/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['private', 'friends', 'internal', 'public'])

    def test_combined_api_anonymous(self):
        response = anonymous_client.get('/api/info/')
        self.assertEqual(response.status_code, 403)

    def test_combined_api(self):
        response = client.get('/api/info/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['availability_policies'], ['private', 'friends', 'internal', 'public'])
        self.assertEqual(response.json()['categories'],
                         ['cat1', 'cat2', 'cat3', 'cat1/subcat1', 'cat1/subcat2', 'cat1/subcat1/subcat3'])
        self.assertEqual(response.json()['tags'], ['tag1', 'tag2', 'tag3'])
        self.assertEqual([p['name'] for p in response.json()['properties']], ['prop1', 'prop2', 'prop3'])
        self.assertEqual(response.json()['domains'], ['example.com'])
