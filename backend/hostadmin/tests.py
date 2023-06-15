from django.test import TestCase

from authentication.models import ToolshedUser
from hostadmin.models import Domain


class DomainTestCase(TestCase):
    def setUp(self):
        admin = ToolshedUser.objects.create_superuser('admin', 'admin@localhost', '')
        admin.set_password('testpassword')
        admin.save()
        example_com = Domain.objects.create(name='example.com', owner=admin, open_registration=True)
        example_com.save()

    def test_domain(self):
        example_com = Domain.objects.get(name='example.com')
        self.assertEqual(example_com.name, 'example.com')
        self.assertEqual(example_com.owner.username, 'admin')
        self.assertEqual(example_com.open_registration, True)
        self.assertEqual(str(example_com), 'example.com')
