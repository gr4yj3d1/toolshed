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

    def __init__(self, **kwargs):
        self.user = kwargs.get('user', None)
        self.header_prefix = kwargs.get('header_prefix', 'Signature ')
        self.bad_signature = kwargs.get('bad_signature', False)

    def build_header(self, method, target, user, payload=None):
        user = user if user is not None else self.user
        if user is None:
            raise ValueError("User must not be None")
        payload_json = json.dumps(payload, separators=(',', ':')) if payload is not None else ''
        signature = user.sign(
            "http://testserver" + target + (payload_json if not self.bad_signature else payload_json[:-2] + "ff"))
        return {'HTTP_AUTHORIZATION': self.header_prefix + str(user) + ':' + signature,
                'content_type': 'application/json'}, payload_json

    def get(self, target, user=None, **kwargs):
        header, payload = self.build_header('GET', target, user)
        return self.base.get(target, **header, **kwargs)

    def post(self, target, user=None, data=None, **kwargs):
        header, payload = self.build_header('POST', target, user, data)
        return self.base.post(target, payload, **header, **kwargs)

    def put(self, target, user=None, data=None, **kwargs):
        header, payload = self.build_header('PUT', target, user, data)
        return self.base.put(target, payload, **header, **kwargs)

    def patch(self, target, user=None, data=None, **kwargs):
        header, payload = self.build_header('PATCH', target, user, data)
        return self.base.patch(target, payload, **header, **kwargs)

    def delete(self, target, user=None, **kwargs):
        header, payload = self.build_header('DELETE', target, user)
        return self.base.delete(target, **header, **kwargs)


class ToolshedTestCase(TestCase):
    f = {}


class UserTestMixin:

    def prepare_users(self):
        self.f['admin'] = ToolshedUser.objects.create_superuser('testadmin', 'testadmin@localhost', 'testpassword')
        self.f['example_com'] = Domain.objects.create(name='example.com', owner=self.f['admin'], open_registration=True)
        self.f['local_user1'] = ToolshedUser.objects.create_user('testuser1', 'test1@abc.de', 'testpassword2',
                                                                 domain=self.f['example_com'].name)
        self.f['local_user2'] = ToolshedUser.objects.create_user('testuser2', 'test2@abc.de', 'testpassword3',
                                                                 domain=self.f['example_com'].name)
        self.f['ext_user1'] = DummyExternalUser('extuser1', 'external.org')
        self.f['ext_user2'] = DummyExternalUser('extuser2', 'external.org')
