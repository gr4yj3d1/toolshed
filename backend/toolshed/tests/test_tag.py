from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.models import Tag, Category

client = SignatureAuthClient()


class TagTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['tag1'] = Tag.objects.create(name='tag1', description='tag1 description', category=self.f['cat1'])
        self.f['tag1'].save()
        self.f['tag2'] = Tag.objects.create(name='tag2', description='tag2 description', category=self.f['cat1'])
        self.f['tag2'].save()
        self.f['tag3'] = Tag.objects.create(name='tag3')
        self.f['tag3'].save()

    def test_tags(self):
        self.assertEqual(len(Tag.objects.all()), 3)
        self.assertEqual(self.f['tag1'].name, 'tag1')
        self.assertEqual(self.f['tag1'].description, 'tag1 description')
        self.assertEqual(self.f['tag1'].category, self.f['cat1'])
        self.assertEqual(self.f['tag2'].name, 'tag2')
        self.assertEqual(self.f['tag2'].description, 'tag2 description')
        self.assertEqual(self.f['tag2'].category, self.f['cat1'])
        self.assertEqual(self.f['tag3'].name, 'tag3')
        self.assertEqual(self.f['tag3'].description, None)
        self.assertEqual(self.f['tag3'].category, None)
        self.assertEqual(str(self.f['tag1']), 'tag1')
        self.assertEqual(str(self.f['tag2']), 'tag2')
        self.assertEqual(str(self.f['tag3']), 'tag3')
        self.assertEqual(self.f['cat1'].tags.count(), 2)
        self.assertEqual(self.f['cat1'].tags.first(), self.f['tag1'])
        self.assertEqual(self.f['cat1'].tags.last(), self.f['tag2'])


class TagApiTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['tag1'] = Tag.objects.create(name='tag1', description='tag1 description', category=self.f['cat1'])
        self.f['tag1'].save()
        self.f['tag2'] = Tag.objects.create(name='tag2', description='tag2 description', category=self.f['cat1'])
        self.f['tag2'].save()
        self.f['tag3'] = Tag.objects.create(name='tag3')
        self.f['tag3'].save()

    def test_get_tags(self):
        reply = client.get('/api/tags/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0], 'tag1')
        self.assertEqual(reply.json()[1], 'tag2')
        self.assertEqual(reply.json()[2], 'tag3')
