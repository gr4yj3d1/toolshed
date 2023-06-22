from django.test import TestCase, Client
from authentication.tests import UserTestCase, SignatureAuthClient
from toolshed.models import Category, Tag, Property

anonymous_client = Client()
client = SignatureAuthClient()


class CombinedApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat2 = Category.objects.create(name='cat2')
        self.cat3 = Category.objects.create(name='cat3')
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')
        self.prop1 = Property.objects.create(name='prop1')
        self.prop2 = Property.objects.create(name='prop2')
        self.prop3 = Property.objects.create(name='prop3')


    def test_domains_anonymous(self):
        response = anonymous_client.get('/api/domains/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['example.com'])

    def test_domains_authenticated(self):
        response = client.get('/api/domains/', self.local_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['example.com'])

    def test_combined_api_anonymous(self):
        response = anonymous_client.get('/api/info/')
        self.assertEqual(response.status_code, 403)

    def test_combined_api(self):
        response = client.get('/api/info/', self.local_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['policies'], ['private', 'friends', 'internal', 'public'])
        self.assertEqual(response.json()['categories'], ['cat1', 'cat2', 'cat3'])
        self.assertEqual(response.json()['tags'], ['tag1', 'tag2', 'tag3'])
        self.assertEqual(response.json()['properties'], ['prop1', 'prop2', 'prop3'])

    def test_policy_api_anonymous(self):
        response = anonymous_client.get('/api/availability_policies/')
        self.assertEqual(response.status_code, 403)

    def test_policy_api(self):
        response = client.get('/api/availability_policies/', self.local_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['private', 'friends', 'internal', 'public'])

