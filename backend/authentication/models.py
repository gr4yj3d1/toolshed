from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db import models
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey


class KnownIdentity(models.Model):
    username = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)

    class Meta:
        unique_together = ('username', 'domain', 'public_key')
        indexes = [
            models.Index(fields=['username', 'domain', 'public_key'], name='identity_idx'),
        ]

    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.username}@{self.domain}"


class ToolshedUserManager(auth.models.BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        domain = extra_fields.pop('domain', 'localhost')
        private_key_hex = extra_fields.pop('private_key', None)
        private_key = SigningKey(bytes.fromhex(private_key_hex)) if private_key_hex else SigningKey.generate()
        public_key = SigningKey(private_key.encode()).verify_key
        extra_fields['private_key'] = private_key.encode(encoder=HexEncoder).decode('utf-8')
        extra_fields['public_identity'] = KnownIdentity.objects.create(
            username=username, domain=domain, public_key=public_key.encode(encoder=HexEncoder).decode('utf-8'))
        user = super().create(username=username, email=email, password=password, domain=domain, **extra_fields)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        return user


class ToolshedUser(AbstractUser):
    domain = models.CharField(max_length=255, default='localhost')
    private_key = models.CharField(max_length=255)
    friends = models.ManyToManyField(KnownIdentity, related_name='friends')
    public_identity = models.ForeignKey(KnownIdentity, on_delete=models.CASCADE, related_name='user')
    objects = ToolshedUserManager()


class FriendRequestOutgoing(models.Model):
    nonce = models.CharField(max_length=255)
    from_user = models.ForeignKey(KnownIdentity, on_delete=models.DO_NOTHING, related_name='friend_requests_outgoing')
    to_username = models.CharField(max_length=255)
    to_domain = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class FriendRequestIncoming(models.Model):
    nonce = models.CharField(max_length=255)
    from_username = models.CharField(max_length=255)
    from_domain = models.CharField(max_length=255)
    to_user = models.ForeignKey(KnownIdentity, on_delete=models.DO_NOTHING, related_name='friend_requests_incoming')
    created_at = models.DateTimeField(auto_now_add=True)
