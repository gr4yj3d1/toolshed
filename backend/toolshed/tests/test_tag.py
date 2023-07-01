from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.models import Tag
from toolshed.tests import TagTestMixin, CategoryTestMixin

client = SignatureAuthClient()


class TagTestCase(TagTestMixin, CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()

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


class TagApiTestCase(TagTestMixin, CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()

    def test_get_tags(self):
        reply = client.get('/api/tags/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0], 'tag1')
        self.assertEqual(reply.json()[1], 'tag2')
        self.assertEqual(reply.json()[2], 'tag3')
