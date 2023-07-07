from toolshed.models import Category, Tag, Property, InventoryItem, ItemProperty


class CategoryTestMixin:
    def prepare_categories(self):
        self.f['cat1'] = Category.objects.create(name='cat1', origin='test')
        self.f['cat2'] = Category.objects.create(name='cat2', origin='test')
        self.f['cat3'] = Category.objects.create(name='cat3', origin='test')
        self.f['subcat1'] = Category.objects.create(name='subcat1', parent=self.f['cat1'], origin='test')
        self.f['subcat2'] = Category.objects.create(name='subcat2', parent=self.f['cat1'], origin='test')
        self.f['subcat3'] = Category.objects.create(name='subcat3', parent=self.f['subcat1'], origin='test')


class TagTestMixin:
    def prepare_tags(self):
        self.f['tag1'] = Tag.objects.create(name='tag1', description='tag1 description', category=self.f['cat1'], origin='test')
        self.f['tag2'] = Tag.objects.create(name='tag2', description='tag2 description', category=self.f['cat1'], origin='test')
        self.f['tag3'] = Tag.objects.create(name='tag3', origin='test')


class PropertyTestMixin:
    def prepare_properties(self):
        self.f['prop1'] = Property.objects.create(name='prop1', origin='test')
        self.f['prop2'] = Property.objects.create(
            name='prop2', description='prop2 description', category=self.f['cat1'], origin='test')
        self.f['prop3'] = Property.objects.create(
            name='prop3', description='prop3 description', category=self.f['cat1'], origin='test')


class InventoryTestMixin(CategoryTestMixin, TagTestMixin, PropertyTestMixin):
    def prepare_inventory(self):
        self.f['local_user1'].friends.add(self.f['local_user2'].public_identity)

        self.f['item1'] = InventoryItem.objects.create(
            owner=self.f['local_user1'], owned_quantity=1, name='test1', description='test', category=self.f['cat1'],
            availability_policy='friends')
        self.f['item2'] = InventoryItem.objects.create(
            owner=self.f['local_user1'], owned_quantity=1, name='test2', description='test2', category=self.f['cat1'],
            availability_policy='friends')
        self.f['item2'].tags.add(self.f['tag1'], through_defaults={})
        self.f['item2'].tags.add(self.f['tag2'], through_defaults={})
        ItemProperty.objects.create(inventory_item=self.f['item2'], property=self.f['prop1'], value='value1').save()
        ItemProperty.objects.create(inventory_item=self.f['item2'], property=self.f['prop2'], value='value2').save()
