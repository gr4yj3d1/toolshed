from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey
from rest_framework import authentication

from authentication.models import KnownIdentity


class SignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authentication_header = request.META.get('HTTP_AUTHORIZATION')

        if not authentication_header:
            return None

        if not authentication_header.startswith('Signature '):
            return None

        signature = authentication_header.split('Signature ')[1]
        author = signature.split(':')[0]
        signature_bytes = bytes.fromhex(signature.split(':')[1])

        if not author or not signature_bytes or len(signature_bytes) != 64:
            return None

        username = author.split('@')[0]
        domain = author.split('@')[1]

        if not username or not domain:
            return None

        signed_data = request.build_absolute_uri()

        if request.method == 'POST':
            signed_data += request.body.decode('utf-8')
        elif request.method == 'PUT':
            signed_data += request.body.decode('utf-8')
        elif request.method == 'PATCH':
            signed_data += request.body.decode('utf-8')

        dummy_key = SigningKey.generate()  # to prevent timing attacks
        # no early return after this point

        try:
            author_identity = KnownIdentity.objects.get(username=username, domain=domain)
            verify_key = VerifyKey(bytes.fromhex(author_identity.public_key))
        except KnownIdentity.DoesNotExist:
            author_identity = None
            verify_key = dummy_key.verify_key

        try:
            verify_key.verify(signed_data.encode('utf-8'), signature_bytes)
            return author_identity, None  # TODO: return user?
        except BadSignatureError:
            return None
