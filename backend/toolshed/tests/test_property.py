from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.models import Property, Category

client = SignatureAuthClient()


class PropertyTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['prop1'] = Property.objects.create(name='prop1')
        self.f['prop1'].save()
        self.f['prop2'] = Property.objects.create(name='prop2', description='prop2 description', category=self.f['cat1'])
        self.f['prop2'].save()
        self.f['prop3'] = Property.objects.create(name='prop3', description='prop3 description', category=self.f['cat1'])
        self.f['prop3'].save()

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


class PropertyApiTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['cat2'] = Category.objects.create(name='cat2')
        self.f['cat2'].save()
        self.f['cat3'] = Category.objects.create(name='cat3')
        self.f['cat3'].save()

    def test_get_properties(self):
        reply = client.get('/api/properties/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 0)
        prop1 = Property.objects.create(name='prop1')
        prop1.save()
