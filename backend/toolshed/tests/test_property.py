from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.models import Property
from toolshed.tests import PropertyTestMixin, CategoryTestMixin

client = SignatureAuthClient()


class PropertyTestCase(PropertyTestMixin, CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_properties()

    def test_properties(self):
        self.assertEqual(len(Property.objects.all()), 3)
        self.assertEqual(self.f['prop1'].name, 'prop1')
        self.assertEqual(self.f['prop1'].description, None)
        self.assertEqual(self.f['prop1'].category, None)
        self.assertEqual(self.f['prop2'].name, 'prop2')
        self.assertEqual(self.f['prop2'].description, 'prop2 description')
        self.assertEqual(self.f['prop2'].category, self.f['cat1'])
        self.assertEqual(self.f['prop3'].name, 'prop3')
        self.assertEqual(self.f['prop3'].description, 'prop3 description')
        self.assertEqual(self.f['prop3'].category, self.f['cat1'])
        self.assertEqual(str(self.f['prop1']), 'prop1')
        self.assertEqual(str(self.f['prop2']), 'prop2')
        self.assertEqual(str(self.f['prop3']), 'prop3')
        self.assertEqual(self.f['cat1'].properties.count(), 2)
        self.assertEqual(self.f['cat1'].properties.first(), self.f['prop2'])
        self.assertEqual(self.f['cat1'].properties.last(), self.f['prop3'])


class PropertyApiTestCase(PropertyTestMixin, CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_properties()

    def test_get_properties(self):
        reply = client.get('/api/properties/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0]['name'], 'prop1')
        self.assertEqual(reply.json()[0]['description'], None)
        self.assertEqual(reply.json()[0]['category'], None)
        self.assertEqual(reply.json()[1]['name'], 'prop2')
        self.assertEqual(reply.json()[1]['description'], 'prop2 description')
        self.assertEqual(reply.json()[1]['category'], 'cat1')
        self.assertEqual(reply.json()[2]['name'], 'prop3')
        self.assertEqual(reply.json()[2]['description'], 'prop3 description')
        self.assertEqual(reply.json()[2]['category'], 'cat1')
