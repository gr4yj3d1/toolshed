from authentication.tests import UserTestCase, SignatureAuthClient
from toolshed.models import Category

client = SignatureAuthClient()


class CategoryTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.cat2 = Category.objects.create(name='cat2')
        self.cat2.save()
        self.cat3 = Category.objects.create(name='cat3')
        self.cat3.save()

    def test_get_categories(self):
        subcat1 = Category.objects.create(name='subcat1', parent=self.cat1)
        subcat1.save()
        subcat2 = Category.objects.create(name='subcat2', parent=self.cat1)
        subcat2.save()
        subcat3 = Category.objects.create(name='subcat3', parent=subcat1)
        subcat3.save()
        self.assertEqual(self.cat1.children.count(), 2)
        self.assertEqual(self.cat1.children.first(), subcat1)
        self.assertEqual(self.cat1.children.last(), subcat2)
        self.assertEqual(subcat1.parent, self.cat1)
        self.assertEqual(subcat2.parent, self.cat1)
        self.assertEqual(subcat3.parent, subcat1)
        self.assertEqual(str(subcat1), 'cat1/subcat1')
        self.assertEqual(str(subcat2), 'cat1/subcat2')
        self.assertEqual(str(subcat3), 'cat1/subcat1/subcat3')


class CategoryApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.cat2 = Category.objects.create(name='cat2')
        self.cat2.save()
        self.cat3 = Category.objects.create(name='cat3')
        self.cat3.save()

    def test_get_categories(self):
        reply = client.get('/api/categories/', self.local_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 3)
        self.assertEqual(reply.json()[0], 'cat1')
        self.assertEqual(reply.json()[1], 'cat2')
        self.assertEqual(reply.json()[2], 'cat3')
