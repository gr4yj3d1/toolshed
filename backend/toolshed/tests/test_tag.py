from authentication.tests import UserTestCase, SignatureAuthClient
from toolshed.models import Tag, Category

client = SignatureAuthClient()


class TagTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.tag1 = Tag.objects.create(name='tag1', description='tag1 description', category=self.cat1)
        self.tag1.save()
        self.tag2 = Tag.objects.create(name='tag2', description='tag2 description', category=self.cat1)
        self.tag2.save()
        self.tag3 = Tag.objects.create(name='tag3')
        self.tag3.save()

    def test_tags(self):
        self.assertEqual(len(Tag.objects.all()), 3)
        self.assertEqual(self.tag1.name, 'tag1')
        self.assertEqual(self.tag1.description, 'tag1 description')
        self.assertEqual(self.tag1.category, self.cat1)
        self.assertEqual(self.tag2.name, 'tag2')
        self.assertEqual(self.tag2.description, 'tag2 description')
        self.assertEqual(self.tag2.category, self.cat1)
        self.assertEqual(self.tag3.name, 'tag3')
        self.assertEqual(self.tag3.description, None)
        self.assertEqual(self.tag3.category, None)
        self.assertEqual(str(self.tag1), 'tag1')
        self.assertEqual(str(self.tag2), 'tag2')
        self.assertEqual(str(self.tag3), 'tag3')
        self.assertEqual(self.cat1.tags.count(), 2)
        self.assertEqual(self.cat1.tags.first(), self.tag1)
        self.assertEqual(self.cat1.tags.last(), self.tag2)


class TagApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.tag1 = Tag.objects.create(name='tag1', description='tag1 description', category=self.cat1)
        self.tag1.save()
        self.tag2 = Tag.objects.create(name='tag2', description='tag2 description', category=self.cat1)
        self.tag2.save()
        self.tag3 = Tag.objects.create(name='tag3')
        self.tag3.save()

    def test_get_tags(self):
        reply = client.get('/api/tags/', self.local_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0], 'tag1')
        self.assertEqual(reply.json()[1], 'tag2')
        self.assertEqual(reply.json()[2], 'tag3')
