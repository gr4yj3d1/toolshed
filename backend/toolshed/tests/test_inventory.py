from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from files.tests import FilesTestMixin
from toolshed.models import InventoryItem, Category
from toolshed.tests import InventoryTestMixin, CategoryTestMixin, TagTestMixin, PropertyTestMixin

client = SignatureAuthClient()


class InventoryApiTestCase(UserTestMixin, InventoryTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()
        self.prepare_properties()
        self.prepare_inventory()

    def test_get_inventory(self):
        reply = client.get('/api/inventory_items/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['name'], 'test1')
        self.assertEqual(reply.json()[0]['description'], 'test')
        self.assertEqual(reply.json()[0]['owned_quantity'], 1)
        self.assertEqual(reply.json()[0]['tags'], [])
        self.assertEqual(reply.json()[0]['properties'], [])
        self.assertEqual(reply.json()[0]['category'], 'cat1')
        self.assertEqual(reply.json()[0]['availability_policy'], 'friends')
        self.assertEqual(reply.json()[1]['name'], 'test2')
        self.assertEqual(reply.json()[1]['description'], 'test2')
        self.assertEqual(reply.json()[1]['owned_quantity'], 1)
        self.assertEqual(reply.json()[1]['tags'], ['tag1', 'tag2'])
        self.assertEqual(reply.json()[1]['properties'],
                         [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}])
        self.assertEqual(reply.json()[1]['category'], 'cat1')
        self.assertEqual(reply.json()[1]['availability_policy'], 'friends')

    def test_post_new_item(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'availability_policy': 'friends',
            'category': 'cat2',
            'name': 'test3',
            'description': 'test',
            'owned_quantity': 1,
            'image': '',
            'tags': ['tag1', 'tag2'],
            'properties': [{'name': 'prop1', 'value': 'value3'}, {'name': 'prop2', 'value': 'value4'}]
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 3)
        item = InventoryItem.objects.get(name='test3')
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, Category.objects.get(name='cat2'))
        self.assertEqual(item.name, 'test3')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.owned_quantity, 1)
        self.assertEqual([t for t in item.tags.all()], [self.f['tag1'], self.f['tag2']])
        self.assertEqual([p for p in item.properties.all()], [self.f['prop1'], self.f['prop2']])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value3', 'value4'])

    def test_post_new_item2(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'availability_policy': 'friends',
            'name': 'test3',
            'description': 'test',
            'owned_quantity': 1,
            'image': '',
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 3)
        item = InventoryItem.objects.get(name='test3')
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, None)
        self.assertEqual(item.name, 'test3')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.owned_quantity, 1)
        self.assertEqual([t for t in item.tags.all()], [])
        self.assertEqual([p for p in item.properties.all()], [])

    def test_post_new_item_empty(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'availability_policy': 'friends',
            'owned_quantity': 1,
            'image': '',
        })
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(InventoryItem.objects.count(), 2)

    def test_post_new_item3(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'availability_policy': 'friends',
            'name': 'test3',
            'description': 'test',
            'owned_quantity': 1,
            'image': '',
            'category': None,
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 3)
        item = InventoryItem.objects.get(name='test3')
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, None)
        self.assertEqual(item.name, 'test3')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.owned_quantity, 1)
        self.assertEqual([t for t in item.tags.all()], [])
        self.assertEqual([p for p in item.properties.all()], [])

    def test_put_item(self):
        reply = client.put('/api/inventory_items/1/', self.f['local_user1'], {
            'availability_policy': 'friends',
            'name': 'test4',
            'description': 'new description',
            'owned_quantity': 100,
            'image': '',
            'tags': ['tag1', 'tag2', 'tag3'],
            'properties': [{'name': 'prop1', 'value': 'value5'}, {'name': 'prop2', 'value': 'value6'},
                           {'name': 'prop3', 'value': 'value7'}]
        })
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(InventoryItem.objects.count(), 2)
        item = InventoryItem.objects.get(id=1)
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, None)
        self.assertEqual(item.name, 'test4')
        self.assertEqual(item.description, 'new description')
        self.assertEqual(item.owned_quantity, 100)
        self.assertEqual([t for t in item.tags.all()], [self.f['tag1'], self.f['tag2'], self.f['tag3']])
        self.assertEqual([p for p in item.properties.all()], [self.f['prop1'], self.f['prop2'], self.f['prop3']])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value5', 'value6', 'value7'])

    def test_patch_item(self):
        reply = client.patch('/api/inventory_items/1/', self.f['local_user1'], {
            'description': 'new description2',
            'category': 'cat1',
            'owned_quantity': 100,
            'tags': ['tag3'],
            'properties': [{'name': 'prop3', 'value': 'value8'}]
        })
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(InventoryItem.objects.count(), 2)
        item = InventoryItem.objects.get(id=1)
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, Category.objects.get(name='cat1'))
        self.assertEqual(item.name, 'test1')
        self.assertEqual(item.description, 'new description2')
        self.assertEqual(item.owned_quantity, 100)
        self.assertEqual([t for t in item.tags.all()], [self.f['tag3']])
        self.assertEqual([p for p in item.properties.all()], [self.f['prop3']])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value8'])

    def test_patch_item2(self):
        reply = client.patch('/api/inventory_items/1/', self.f['local_user1'], {
            'description': 'new description2',
            'category': None,
            'owned_quantity': 100,
            'tags': [],
            'properties': []
        })
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(InventoryItem.objects.count(), 2)
        item = InventoryItem.objects.get(id=1)
        self.assertEqual(item.availability_policy, 'friends')
        self.assertEqual(item.category, None)
        self.assertEqual(item.name, 'test1')
        self.assertEqual(item.description, 'new description2')
        self.assertEqual(item.owned_quantity, 100)
        self.assertEqual([t for t in item.tags.all()], [])
        self.assertEqual([p for p in item.properties.all()], [])

    def test_delete_item(self):
        reply = client.delete('/api/inventory_items/1/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 204)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get(id=2).name, 'test2')
        self.assertEqual(InventoryItem.objects.filter(name='test1').count(), 0)

    def test_search_items(self):
        reply = client.get('/api/search/?query=test', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['name'], 'test1')
        self.assertEqual(reply.json()[0]['description'], 'test')
        self.assertEqual(reply.json()[0]['owned_quantity'], 1)
        self.assertEqual(reply.json()[0]['tags'], [])
        self.assertEqual(reply.json()[0]['properties'], [])
        self.assertEqual(reply.json()[0]['category'], 'cat1')
        self.assertEqual(reply.json()[0]['availability_policy'], 'friends')
        self.assertEqual(reply.json()[1]['name'], 'test2')
        self.assertEqual(reply.json()[1]['description'], 'test2')
        self.assertEqual(reply.json()[1]['owned_quantity'], 1)
        self.assertEqual(reply.json()[1]['tags'], ['tag1', 'tag2'])
        self.assertEqual(reply.json()[1]['properties'],
                         [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}])
        self.assertEqual(reply.json()[1]['category'], 'cat1')
        self.assertEqual(reply.json()[1]['availability_policy'], 'friends')

    def test_search_items2(self):
        reply = client.get('/api/search/?query=test', self.f['local_user2'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['name'], 'test1')
        self.assertEqual(reply.json()[1]['name'], 'test2')

    def test_search_items_fail(self):
        reply = client.get('/api/search/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(reply.json()['error'], 'No query provided.')

    def test_search_items_fail2(self):
        reply = client.get('/api/search/?query=test', self.f['ext_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 0)


class TestInventoryItemWithFileApiTestCase(UserTestMixin, FilesTestMixin, InventoryTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.prepare_categories()
        self.prepare_tags()
        self.prepare_properties()
        self.prepare_files()
        self.prepare_inventory()

    def test_post_item_with_file_id(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'name': 'test4',
            'description': 'test',
            'category': 'cat1',
            'owned_quantity': 1,
            'tags': ['tag1', 'tag2'],
            'properties': [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}],
            'files': [self.f['test_file1'].id]
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 3)
        item = InventoryItem.objects.get(id=3)
        self.assertEqual(item.availability_policy, 'private')
        self.assertEqual(item.category, Category.objects.get(name='cat1'))
        self.assertEqual(item.name, 'test4')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.owned_quantity, 1)
        self.assertEqual([t for t in item.tags.all()], [self.f['tag1'], self.f['tag2']])
        self.assertEqual([p for p in item.properties.all()], [self.f['prop1'], self.f['prop2']])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value1', 'value2'])
        self.assertEqual([f for f in item.files.all()], [self.f['test_file1']])

    def test_post_item_with_encoded_file(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'name': 'test4',
            'description': 'test',
            'category': 'cat1',
            'owned_quantity': 1,
            'tags': ['tag1', 'tag2'],
            'properties': [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}],
            'files': [{'data': self.f['encoded_content3'], 'mime_type': 'text/plain'}]
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 3)
        item = InventoryItem.objects.get(id=3)
        self.assertEqual(item.availability_policy, 'private')
        self.assertEqual(item.category, Category.objects.get(name='cat1'))
        self.assertEqual(item.name, 'test4')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.owned_quantity, 1)
        self.assertEqual([t for t in item.tags.all()], [self.f['tag1'], self.f['tag2']])
        self.assertEqual([p for p in item.properties.all()], [self.f['prop1'], self.f['prop2']])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value1', 'value2'])
        self.assertEqual([f for f in item.files.all()], [self.f['test_file3']])

    def test_post_item_with_file_id_fail(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'name': 'test4',
            'description': 'test',
            'category': 'cat1',
            'owned_quantity': 1,
            'tags': ['tag1', 'tag2'],
            'properties': [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}],
            'files': [99999]
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_item_with_encoded_file_fail(self):
        reply = client.post('/api/inventory_items/', self.f['local_user1'], {
            'name': 'test4',
            'description': 'test',
            'category': 'cat1',
            'owned_quantity': 1,
            'tags': ['tag1', 'tag2'],
            'properties': [{'name': 'prop1', 'value': 'value1'}, {'name': 'prop2', 'value': 'value2'}],
            'files': [{'data': self.f['encoded_content3']}]
        })
        self.assertEqual(reply.status_code, 400)