from authentication.tests import UserTestCase, SignatureAuthClient
from toolshed.models import Property, Category

client = SignatureAuthClient()


class PropertyTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.prop1 = Property.objects.create(name='prop1')
        self.prop1.save()
        self.prop2 = Property.objects.create(name='prop2', description='prop2 description', category=self.cat1)
        self.prop2.save()
        self.prop3 = Property.objects.create(name='prop3', description='prop3 description', category=self.cat1)
        self.prop3.save()

    def test_properties(self):
        self.assertEqual(len(Property.objects.all()), 3)
        self.assertEqual(self.prop1.name, 'prop1')
        self.assertEqual(self.prop1.description, None)
        self.assertEqual(self.prop1.category, None)
        self.assertEqual(self.prop2.name, 'prop2')
        self.assertEqual(self.prop2.description, 'prop2 description')
        self.assertEqual(self.prop2.category, self.cat1)
        self.assertEqual(self.prop3.name, 'prop3')
        self.assertEqual(self.prop3.description, 'prop3 description')
        self.assertEqual(self.prop3.category, self.cat1)
        self.assertEqual(str(self.prop1), 'prop1')
        self.assertEqual(str(self.prop2), 'prop2')
        self.assertEqual(str(self.prop3), 'prop3')
        self.assertEqual(self.cat1.properties.count(), 2)
        self.assertEqual(self.cat1.properties.first(), self.prop2)
        self.assertEqual(self.cat1.properties.last(), self.prop3)


class PropertyApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.cat2 = Category.objects.create(name='cat2')
        self.cat2.save()
        self.cat3 = Category.objects.create(name='cat3')
        self.cat3.save()

    def test_get_properties(self):
        reply = client.get('/api/properties/', self.local_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 0)
        prop1 = Property.objects.create(name='prop1')
        prop1.save()
