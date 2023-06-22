from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.utils import IntegrityError
from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey


class KnownIdentity(models.Model):
    username = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    friends = models.ManyToManyField('self', symmetrical=True)

    class Meta:
        unique_together = ('username', 'domain')
        indexes = [
            models.Index(fields=['username', 'domain'], name='identity_idx'),
        ]

    def __str__(self):
        return f"{self.username}@{self.domain}"

    def is_authenticated(self):
        return True

    def verify(self, message, signature):
        if len(signature) != 128 or type(signature) != str:
            raise TypeError('Signature must be 128 characters long and a string')
        if type(message) != str:
            raise TypeError('Message must be a string')
        try:
            VerifyKey(bytes.fromhex(self.public_key)).verify(message.encode('utf-8'), bytes.fromhex(signature))
            return True
        except BadSignatureError:
            return False


class ToolshedUserManager(auth.models.BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        domain = extra_fields.pop('domain', 'localhost')
        private_key_hex = extra_fields.pop('private_key', None)
        if private_key_hex and type(private_key_hex) != str:
            raise TypeError('Private key must be a string or no private key must be provided')
        if private_key_hex and len(private_key_hex) != 64:
            raise ValueError('Private key must be 64 characters long or no private key must be provided')
        if private_key_hex and not all(c in '0123456789abcdef' for c in private_key_hex):
            raise ValueError('Private key must be a hexadecimal string or no private key must be provided')
        private_key = SigningKey(bytes.fromhex(private_key_hex)) if private_key_hex else SigningKey.generate()
        public_key = SigningKey(private_key.encode()).verify_key
        extra_fields['private_key'] = private_key.encode(encoder=HexEncoder).decode('utf-8')
        try:
            with transaction.atomic():
                extra_fields['public_identity'] = identity = KnownIdentity.objects.get_or_create(
                    username=username, domain=domain, public_key=public_key.encode(encoder=HexEncoder).decode('utf-8'))[0]
                try:
                    with transaction.atomic():
                        user = super().create(username=username, email=email, password=password, domain=domain,
                                              **extra_fields)
                        user.set_password(password)
                        user.save()
                except IntegrityError:
                    identity.delete()
                    raise ValueError('Username or email already exists')
                else:
                    return user
        except IntegrityError:
            raise ValueError('Username already exists')

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class ToolshedUser(AbstractUser):
    email = models.EmailField(unique=True)
    domain = models.CharField(max_length=255, default='localhost')
    private_key = models.CharField(max_length=255)
    public_identity = models.ForeignKey(KnownIdentity, on_delete=models.CASCADE, related_name='user')
    objects = ToolshedUserManager()

    class Meta:
        unique_together = [('username', 'domain'), ['email']]
        indexes = [
            models.Index(fields=['username', 'domain'], name='user_idx'),
        ]

    def __str__(self):
        return f"{self.username}@{self.domain}"

    @property
    def friends(self):
        return self.public_identity.friends

    def sign(self, message):
        if type(message) != str:
            raise TypeError('Message must be a string')
        private_key = SigningKey(self.private_key.encode(), encoder=HexEncoder)
        return private_key.sign(message.encode('utf-8'), encoder=HexEncoder).signature.decode('utf-8')

    def public_key(self):
        return self.public_identity.public_key


class FriendRequestOutgoing(models.Model):
    secret = models.CharField(max_length=255)
    befriender_user = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='friend_requests_outgoing')
    befriendee_username = models.CharField(max_length=255)
    befriendee_domain = models.CharField(max_length=255)


class FriendRequestIncoming(models.Model):
    secret = models.CharField(max_length=255)
    befriender_username = models.CharField(max_length=255)
    befriender_domain = models.CharField(max_length=255)
    befriender_public_key = models.CharField(max_length=255)
    befriendee_user = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='friend_requests_incoming')
    created_at = models.DateTimeField(auto_now_add=True)
