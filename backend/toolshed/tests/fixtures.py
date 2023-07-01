from toolshed.models import Category, Tag, Property, InventoryItem, ItemProperty


class InventoryTestMixin:
    def prepare_inventory(self):
        self.f['local_user1'].friends.add(self.f['local_user2'].public_identity)
        self.f['cat1'] = Category.objects.create(name='cat1')
        self.f['cat2'] = Category.objects.create(name='cat2')
        self.f['tag1'] = Tag.objects.create(name='tag1', category=self.f['cat1'])
        self.f['tag2'] = Tag.objects.create(name='tag2', category=self.f['cat1'])
        self.f['tag3'] = Tag.objects.create(name='tag3')
        self.f['prop1'] = Property.objects.create(name='prop1')
        self.f['prop2'] = Property.objects.create(name='prop2')
        self.f['prop3'] = Property.objects.create(name='prop3', category=self.f['cat1'])

        self.f['item1'] = InventoryItem.objects.create(owner=self.f['local_user1'], owned_quantity=1, name='test1',
                                                  description='test',
                                                  category=self.f['cat1'], availability_policy='friends')
        self.f['item2'] = InventoryItem.objects.create(owner=self.f['local_user1'], owned_quantity=1, name='test2',
                                                  description='test2',
                                                  category=self.f['cat1'], availability_policy='friends')
        self.f['item2'].tags.add(self.f['tag1'], through_defaults={})
        self.f['item2'].tags.add(self.f['tag2'], through_defaults={})
        ItemProperty.objects.create(inventory_item=self.f['item2'], property=self.f['prop1'], value='value1').save()
        ItemProperty.objects.create(inventory_item=self.f['item2'], property=self.f['prop2'], value='value2').save()
