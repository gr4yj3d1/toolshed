from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from toolshed.models import Category

client = SignatureAuthClient()


class CategoryTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['cat2'] = Category.objects.create(name='cat2')
        self.f['cat2'].save()
        self.f['cat3'] = Category.objects.create(name='cat3')
        self.f['cat3'].save()

    def test_get_categories(self):
        subcat1 = Category.objects.create(name='subcat1', parent=self.f['cat1'])
        subcat1.save()
        subcat2 = Category.objects.create(name='subcat2', parent=self.f['cat1'])
        subcat2.save()
        subcat3 = Category.objects.create(name='subcat3', parent=subcat1)
        subcat3.save()
        self.assertEqual(self.f['cat1'].children.count(), 2)
        self.assertEqual(self.f['cat1'].children.first(), subcat1)
        self.assertEqual(self.f['cat1'].children.last(), subcat2)
        self.assertEqual(subcat1.parent, self.f['cat1'])
        self.assertEqual(subcat2.parent, self.f['cat1'])
        self.assertEqual(subcat3.parent, subcat1)
        self.assertEqual(str(subcat1), 'cat1/subcat1')
        self.assertEqual(str(subcat2), 'cat1/subcat2')
        self.assertEqual(str(subcat3), 'cat1/subcat1/subcat3')


class CategoryApiTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat1'].save()
        self.f['cat2'] = Category.objects.create(name='cat2')
        self.f['cat2'].save()
        self.f['cat3'] = Category.objects.create(name='cat3')
        self.f['cat3'].save()

    def test_get_categories(self):
        reply = client.get('/api/categories/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0], 'cat1')
        self.assertEqual(reply.json()[1], 'cat2')
        self.assertEqual(reply.json()[2], 'cat3')
