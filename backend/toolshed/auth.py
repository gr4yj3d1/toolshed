from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey
from rest_framework import authentication

from authentication.models import KnownIdentity, ToolshedUser


def split_userhandle_or_throw(userhandle):
    if '@' not in userhandle:
        raise ValueError('Userhandle must be in the format username@domain')
    username, domain = userhandle.split('@')
    if not username:
        raise ValueError('Username cannot be empty')
    if not domain:
        raise ValueError('Domain cannot be empty')
    return username, domain


def verify_incoming_friend_request(request, raw_request):
    authentication_header = request.META.get('HTTP_AUTHORIZATION')

    if not authentication_header:
        return False

    if not authentication_header.startswith('Signature '):
        return False

    signature = authentication_header.split('Signature ')[1]
    author = signature.split(':')[0]
    signature_bytes = bytes.fromhex(signature.split(':')[1])

    if not author or not signature_bytes or len(signature_bytes) != 64:
        return False

    signed_data = request.build_absolute_uri()

    if request.method == 'POST':
        signed_data += raw_request
    elif request.method == 'PUT':
        signed_data += raw_request
    elif request.method == 'PATCH':
        signed_data += raw_request

    befriender = request.data['befriender']
    befriender_key = request.data['befriender_key']

    if not befriender or not befriender_key:
        return False

    if author != befriender:
        return False

    if len(befriender_key) != 64:
        return False

    verify_key = VerifyKey(bytes.fromhex(befriender_key))

    try:
        verify_key.verify(signed_data.encode('utf-8'), signature_bytes)
        return True
    except BadSignatureError:
        return False


def authenticate_request_against_known_identities(request, raw_request):
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

    username, domain = split_userhandle_or_throw(author)

    signed_data = request.build_absolute_uri()

    if request.method == 'POST':
        signed_data += raw_request
    elif request.method == 'PUT':
        signed_data += raw_request
    elif request.method == 'PATCH':
        signed_data += raw_request

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
        return author_identity
    except BadSignatureError:
        return None


def authenticate_request_against_local_users(request, raw_request):
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

    username, domain = split_userhandle_or_throw(author)

    signed_data = request.build_absolute_uri()

    if request.method == 'POST':
        signed_data += raw_request
    elif request.method == 'PUT':
        signed_data += raw_request
    elif request.method == 'PATCH':
        signed_data += raw_request

    dummy_key = SigningKey.generate()  # to prevent timing attacks
    # no early return after this point

    try:
        author_user = ToolshedUser.objects.get(username=username, domain=domain)
        verify_key = VerifyKey(bytes.fromhex(author_user.public_identity.public_key))
    except ToolshedUser.DoesNotExist:
        author_user = None
        verify_key = dummy_key.verify_key

    try:
        verify_key.verify(signed_data.encode('utf-8'), signature_bytes)
        return author_user
    except BadSignatureError:
        return None


class SignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return authenticate_request_against_known_identities(
            request, request.body.decode('utf-8')), None  # TODO: return user?
