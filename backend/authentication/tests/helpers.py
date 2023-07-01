import json

from django.test import TestCase, Client
from nacl.encoding import HexEncoder

from authentication.models import ToolshedUser, KnownIdentity
from hostadmin.models import Domain
from nacl.signing import SigningKey


class DummyExternalUser:
    def __init__(self, username, domain, known=True):
        self.username = username
        self.domain = domain
        self.__signing_key = SigningKey.generate()
        self.public_identity = KnownIdentity.objects.get_or_create(
            username=username,
            domain=domain,
            public_key=self.public_key())[0] if known else None

    def __str__(self):
        return self.username + '@' + self.domain

    def sign(self, message):
        return self.__signing_key.sign(message.encode('utf-8'), encoder=HexEncoder).signature.decode('utf-8')

    def public_key(self):
        return self.__signing_key.verify_key.encode(encoder=HexEncoder).decode('utf-8')

    @property
    def friends(self):
        return self.public_identity.friends


class SignatureAuthClient:
    base = Client(SERVER_NAME='testserver')

    def get(self, target, user, **kwargs):
        if user is None:
            raise ValueError("User must not be None")
        signature = user.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.get(target, **header, **kwargs)

    def post(self, target, user, data, **kwargs):
        if user is None:
            raise ValueError("User must not be None")
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.post(target, json_data, **header, content_type='application/json', **kwargs)

    def put(self, target, user, data, **kwargs):
        if user is None:
            raise ValueError("User must not be None")
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.put(target, json_data, **header, content_type='application/json', **kwargs)

    def patch(self, target, user, data, **kwargs):
        if user is None:
            raise ValueError("User must not be None")
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.patch(target, json_data, **header, content_type='application/json', **kwargs)

    def delete(self, target, user, **kwargs):
        if user is None:
            raise ValueError("User must not be None")
        signature = user.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.delete(target, **header, **kwargs)


class ToolshedTestCase(TestCase):
    f = {}


class UserTestMixin:

    def prepare_users(self):
        self.f['admin'] = ToolshedUser.objects.create_superuser('testadmin', 'testadmin@localhost', '')
        self.f['admin'].set_password('testpassword')
        self.f['admin'].save()
        self.f['example_com'] = Domain.objects.create(name='example.com', owner=self.f['admin'], open_registration=True)
        self.f['example_com'].save()
        self.f['local_user1'] = ToolshedUser.objects.create_user('testuser1', 'test1@abc.de', '',
                                                                 domain=self.f['example_com'].name)
        self.f['local_user1'].set_password('testpassword2')
        self.f['local_user1'].save()
        self.f['local_user2'] = ToolshedUser.objects.create_user('testuser2', 'test2@abc.de', '',
                                                                 domain=self.f['example_com'].name)
        self.f['local_user2'].set_password('testpassword3')
        self.f['local_user2'].save()
        self.f['ext_user1'] = DummyExternalUser('extuser1', 'external.org')
        self.f['ext_user2'] = DummyExternalUser('extuser2', 'external.org')
