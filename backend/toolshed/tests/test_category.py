from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.tests import CategoryTestMixin

client = SignatureAuthClient()


class CategoryTestCase(CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()

    def test_get_categories(self):
        self.assertEqual(self.f['cat1'].children.count(), 2)
        self.assertEqual(self.f['cat1'].children.first(), self.f['subcat1'])
        self.assertEqual(self.f['cat1'].children.last(), self.f['subcat2'])
        self.assertEqual(self.f['subcat1'].parent, self.f['cat1'])
        self.assertEqual(self.f['subcat2'].parent, self.f['cat1'])
        self.assertEqual(self.f['subcat1'].children.count(), 1)
        self.assertEqual(str(self.f['subcat1']), 'cat1/subcat1')
        self.assertEqual(str(self.f['subcat2']), 'cat1/subcat2')
        self.assertEqual(str(self.f['subcat3']), 'cat1/subcat1/subcat3')


class CategoryApiTestCase(CategoryTestMixin, UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()

    def test_get_categories(self):
        reply = client.get('/api/categories/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 6)
        self.assertEqual(reply.json()[0], 'cat1')
        self.assertEqual(reply.json()[1], 'cat2')
        self.assertEqual(reply.json()[2], 'cat3')
        self.assertEqual(reply.json()[3], 'cat1/subcat1')
        self.assertEqual(reply.json()[4], 'cat1/subcat2')
        self.assertEqual(reply.json()[5], 'cat1/subcat1/subcat3')
