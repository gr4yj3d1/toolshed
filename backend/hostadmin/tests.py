from authentication.models import ToolshedUser
from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from hostadmin.models import Domain
from django.test import Client

from toolshed.tests import CategoryTestMixin, TagTestMixin, PropertyTestMixin

anonymous_client = Client()
client = SignatureAuthClient()


class DomainTestCase(ToolshedTestCase):
    def setUp(self):
        admin = ToolshedUser.objects.create_superuser('admin', 'admin@localhost', 'testpassword')
        example_com = Domain.objects.create(name='example.com', owner=admin, open_registration=True)

    def test_domain(self):
        example_com = Domain.objects.get(name='example.com')
        self.assertEqual(example_com.name, 'example.com')
        self.assertEqual(example_com.owner.username, 'admin')
        self.assertEqual(example_com.open_registration, True)
        self.assertEqual(str(example_com), 'example.com')


class DomainApiTestCase(UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()

    def test_get_domains(self):
        response = client.get('/api/domains/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['example.com'])

    def test_admin_get_domains_fail(self):
        response = client.get('/admin/domains/', self.f['local_user1'])
        self.assertEqual(response.status_code, 403)

    def test_admin_get_domains(self):
        response = client.get('/admin/domains/', self.f['admin'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'example.com')
        self.assertEqual(response.json()[0]['owner'], str(self.f['admin']))
        self.assertEqual(response.json()[0]['open_registration'], True)

    def test_admin_create_domain(self):
        response = client.post('/admin/domains/', self.f['admin'],
                               {'name': 'example2.com', 'owner': 'local_user1', 'open_registration': False})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'example2.com')
        self.assertEqual(response.json()['owner'], str(self.f['admin']))
        self.assertEqual(response.json()['open_registration'], False)
        self.assertEqual(Domain.objects.count(), 2)
        self.assertEqual(Domain.objects.get(name='example2.com').owner, self.f['admin'])
        self.assertEqual(Domain.objects.get(name='example2.com').open_registration, False)

    def test_admin_create_domain_fail(self):
        response = client.post('/admin/domains/', self.f['local_user1'],
                               {'name': 'example2.com', 'owner': 'local_user1', 'open_registration': False})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Domain.objects.count(), 1)

    def test_admin_update_domain(self):
        response = client.put('/admin/domains/1/', self.f['admin'],
                              {'name': 'example.com', 'owner': 'local_user1', 'open_registration': False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'example.com')
        self.assertEqual(response.json()['owner'], str(self.f['admin']))
        self.assertEqual(response.json()['open_registration'], False)
        self.assertEqual(Domain.objects.count(), 1)
        self.assertEqual(Domain.objects.get(name='example.com').owner, self.f['admin'])
        self.assertEqual(Domain.objects.get(name='example.com').open_registration, False)

    def test_admin_update_domain_fail(self):
        response = client.put('/admin/domains/1/', self.f['local_user1'],
                              {'name': 'example.com', 'owner': 'local_user1', 'open_registration': False})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Domain.objects.count(), 1)

    def test_admin_delete_domain(self):
        response = client.delete('/admin/domains/1/', self.f['admin'])
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Domain.objects.count(), 0)

    def test_admin_delete_domain_fail(self):
        response = client.delete('/admin/domains/1/', self.f['local_user1'])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Domain.objects.count(), 1)


class CategoryApiTestCase(UserTestMixin, CategoryTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()

    def test_get_categories(self):
        response = client.get('/api/categories/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         ["cat1", "cat2", "cat3", "cat1/subcat1", "cat1/subcat2", "cat1/subcat1/subcat3"])

    def test_admin_get_categories_fail(self):
        response = client.get('/admin/categories/', self.f['local_user1'])
        self.assertEqual(response.status_code, 403)

    def test_admin_get_categories(self):
        response = client.get('/admin/categories/', self.f['admin'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)
        self.assertEqual(response.json()[0]['name'], 'cat1')
        self.assertEqual(response.json()[1]['name'], 'cat2')
        self.assertEqual(response.json()[2]['name'], 'cat3')
        self.assertEqual(response.json()[3]['name'], 'subcat1')
        self.assertEqual(response.json()[3]['parent'], 'cat1')
        self.assertEqual(response.json()[4]['name'], 'subcat2')
        self.assertEqual(response.json()[4]['parent'], 'cat1')
        self.assertEqual(response.json()[5]['name'], 'subcat3')
        self.assertEqual(response.json()[5]['parent'], 'subcat1')

    def test_admin_create_category(self):
        response = client.post('/admin/categories/', self.f['admin'], {'name': 'cat4'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'cat4')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['parent'], None)
        self.assertEqual(response.json()['origin'], 'api')

    def test_admin_post_subcategory(self):
        response = client.post('/admin/categories/', self.f['admin'], {'name': 'subcat4', 'parent': 'cat1'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'subcat4')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['parent'], 'cat1')
        self.assertEqual(response.json()['origin'], 'api')

    def test_admin_put_category(self):
        response = client.put('/admin/categories/1/', self.f['admin'], {'name': 'cat5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'cat5')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['parent'], None)
        self.assertEqual(response.json()['origin'], 'test')

    def test_admin_patch_category(self):
        response = client.patch('/admin/categories/1/', self.f['admin'], {'name': 'cat5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'cat5')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['parent'], None)
        self.assertEqual(response.json()['origin'], 'test')

    def test_admin_delete_category(self):
        response = client.delete('/admin/categories/2/', self.f['admin'])
        self.assertEqual(response.status_code, 204)


class TagApiTestCase(UserTestMixin, CategoryTestMixin, TagTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()

    def test_get_tags(self):
        response = client.get('/api/tags/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["tag1", "tag2", "tag3"])

    def test_admin_get_tags_fail(self):
        response = client.get('/admin/tags/', self.f['local_user1'])
        self.assertEqual(response.status_code, 403)

    def test_admin_get_tags(self):
        response = client.get('/admin/tags/', self.f['admin'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['name'], 'tag1')

    def test_admin_create_tag(self):
        response = client.post('/admin/tags/', self.f['admin'], {'name': 'tag4'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'tag4')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['origin'], 'api')
        self.assertEqual(response.json()['category'], None)

    def test_admin_put_tag(self):
        response = client.put('/admin/tags/1/', self.f['admin'], {'name': 'tag5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'tag5')
        self.assertEqual(response.json()['description'], 'tag1 description')
        self.assertEqual(response.json()['origin'], 'test')
        self.assertEqual(response.json()['category'], 'cat1')

    def test_admin_patch_tag(self):
        response = client.patch('/admin/tags/1/', self.f['admin'], {'name': 'tag5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'tag5')
        self.assertEqual(response.json()['description'], 'tag1 description')
        self.assertEqual(response.json()['origin'], 'test')
        self.assertEqual(response.json()['category'], 'cat1')

    def test_admin_delete_tag(self):
        response = client.delete('/admin/tags/2/', self.f['admin'])
        self.assertEqual(response.status_code, 204)


class PropertyApiTestCase(UserTestMixin, CategoryTestMixin, PropertyTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_properties()

    def test_get_properties(self):
        response = client.get('/api/properties/', self.f['local_user1'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['name'], 'prop1')
        self.assertEqual(response.json()[1]['name'], 'prop2')
        self.assertEqual(response.json()[2]['name'], 'prop3')

    def test_admin_get_properties_fail(self):
        response = client.get('/admin/properties/', self.f['local_user1'])
        self.assertEqual(response.status_code, 403)

    def test_admin_get_properties(self):
        response = client.get('/admin/properties/', self.f['admin'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['name'], 'prop1')
        self.assertEqual(response.json()[1]['name'], 'prop2')
        self.assertEqual(response.json()[2]['name'], 'prop3')

    def test_admin_create_property(self):
        response = client.post('/admin/properties/', self.f['admin'], {'name': 'prop4'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'prop4')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['origin'], 'api')
        self.assertEqual(response.json()['category'], None)
        self.assertEqual(response.json()['unit_symbol'], None)
        self.assertEqual(response.json()['unit_name'], None)
        self.assertEqual(response.json()['unit_name_plural'], None)
        self.assertEqual(response.json()['base2_prefix'], False)
        self.assertEqual(response.json()['dimensions'], 1)

    #        self.assertEqual(response.json()['sort_lexicographically'], False)

    def test_admin_put_property(self):
        response = client.put('/admin/properties/1/', self.f['admin'], {'name': 'prop5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'prop5')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['origin'], 'test')
        self.assertEqual(response.json()['category'], None)
        self.assertEqual(response.json()['unit_symbol'], None)
        self.assertEqual(response.json()['unit_name'], None)
        self.assertEqual(response.json()['unit_name_plural'], None)
        self.assertEqual(response.json()['base2_prefix'], False)
        self.assertEqual(response.json()['dimensions'], 1)

    #       self.assertEqual(response.json()['sort_lexicographically'], False)

    def test_admin_patch_property(self):
        response = client.patch('/admin/properties/1/', self.f['admin'], {'name': 'prop5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'prop5')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['origin'], 'test')
        self.assertEqual(response.json()['category'], None)
        self.assertEqual(response.json()['unit_symbol'], None)
        self.assertEqual(response.json()['unit_name'], None)
        self.assertEqual(response.json()['unit_name_plural'], None)
        self.assertEqual(response.json()['base2_prefix'], False)
        self.assertEqual(response.json()['dimensions'], 1)

    #       self.assertEqual(response.json()['sort_lexicographically'], False)

    def test_admin_delete_property(self):
        response = client.delete('/admin/properties/2/', self.f['admin'])
        self.assertEqual(response.status_code, 204)
