from authentication.models import ToolshedUser
from authentication.tests import UserTestCase, SignatureAuthClient
from toolshed.models import InventoryItem, Tag, Property, ItemProperty, Category

client = SignatureAuthClient()


class InventoryTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.user1 = ToolshedUser.objects.get(username="testuser")
        self.user2 = ToolshedUser.objects.get(username="testuser2")
        self.user1.friends.add(self.user2.public_identity)
        self.user2.friends.add(self.user1.public_identity)
        self.cat1 = Category.objects.create(name='cat1')
        self.cat1.save()
        self.cat2 = Category.objects.create(name='cat2')
        self.cat2.save()
        self.tag1 = Tag.objects.create(name='tag1', category=self.cat1)
        self.tag1.save()
        self.tag2 = Tag.objects.create(name='tag2', category=self.cat1)
        self.tag2.save()
        self.tag3 = Tag.objects.create(name='tag3')
        self.tag3.save()
        self.prop1 = Property.objects.create(name='prop1')
        self.prop1.save()
        self.prop2 = Property.objects.create(name='prop2')
        self.prop2.save()
        self.prop3 = Property.objects.create(name='prop3', category=self.cat1)
        self.prop3.save()

        InventoryItem.objects.create(owner=self.user1, owned_quantity=1, name='test1', description='test',
                                     category=self.cat1, availability_policy='friends').save()
        item2 = InventoryItem.objects.create(owner=self.user1, owned_quantity=1, name='test2', description='test2',
                                             category=self.cat1, availability_policy='friends')
        item2.save()
        item2.tags.add(self.tag1, through_defaults={})
        item2.tags.add(self.tag2, through_defaults={})
        ItemProperty.objects.create(inventory_item=item2, property=self.prop1, value='value1').save()
        ItemProperty.objects.create(inventory_item=item2, property=self.prop2, value='value2').save()

    def test_get_inventory(self):
        reply = client.get('/api/inventory_items/', self.user1)
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
        reply = client.post('/api/inventory_items/', self.user1, {
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
        self.assertEqual([t for t in item.tags.all()], [self.tag1, self.tag2])
        self.assertEqual([p for p in item.properties.all()], [self.prop1, self.prop2])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value3', 'value4'])

    def test_post_new_item2(self):
        reply = client.post('/api/inventory_items/', self.user1, {
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

    def test_post_new_item3(self):
        reply = client.post('/api/inventory_items/', self.user1, {
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
        reply = client.put('/api/inventory_items/1/', self.user1, {
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
        self.assertEqual([t for t in item.tags.all()], [self.tag1, self.tag2, self.tag3])
        self.assertEqual([p for p in item.properties.all()], [self.prop1, self.prop2, self.prop3])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value5', 'value6', 'value7'])

    def test_patch_item(self):
        reply = client.patch('/api/inventory_items/1/', self.user1, {
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
        self.assertEqual([t for t in item.tags.all()], [self.tag3])
        self.assertEqual([p for p in item.properties.all()], [self.prop3])
        self.assertEqual([p.value for p in item.itemproperty_set.all()], ['value8'])

    def test_patch_item2(self):
        reply = client.patch('/api/inventory_items/1/', self.user1, {
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
        reply = client.delete('/api/inventory_items/1/', self.user1)
        self.assertEqual(reply.status_code, 204)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get(id=2).name, 'test2')
        self.assertEqual(InventoryItem.objects.filter(name='test1').count(), 0)

    def test_search_items(self):
        reply = client.get('/api/search/?query=test', self.user1)
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
        reply = client.get('/api/search/?query=test', self.user2)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['name'], 'test1')
        self.assertEqual(reply.json()[1]['name'], 'test2')

    def test_search_items_fail(self):
        reply = client.get('/api/search/', self.user1)
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(reply.json()['error'], 'No query provided.')

    def test_search_items_fail2(self):
        reply = client.get('/api/search/?query=test', self.ext_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 0)
