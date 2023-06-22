from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
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


def verify_request(request, raw_request_body):
    authentication_header = request.META.get('HTTP_AUTHORIZATION')

    if not authentication_header:
        raise ValueError('No authentication header provided')

    if not authentication_header.startswith('Signature '):
        raise ValueError('Authorization header must be in the format "Signature author@domain:signature_hex[128]"')

    signature = authentication_header.split('Signature ')[1]

    if ':' not in signature:
        raise ValueError('Authorization header must be in the format "Signature author@domain:signature_hex[128]"')

    author = signature.split(':')[0]
    signature_bytes_hex = signature.split(':')[1]

    if not author or not signature_bytes_hex or len(signature_bytes_hex) != 128:
        raise ValueError('Authorization header must be in the format "Signature author@domain:signature_hex[128]"')

    username, domain = split_userhandle_or_throw(author)

    signed_data = request.build_absolute_uri()

    if request.method == 'POST':
        signed_data += raw_request_body
    elif request.method == 'PUT':
        signed_data += raw_request_body
    elif request.method == 'PATCH':
        signed_data += raw_request_body

    return username, domain, signed_data, signature_bytes_hex


def verify_incoming_friend_request(request, raw_request_body):
    try:
        username, domain, signed_data, signature_bytes_hex = verify_request(request, raw_request_body)
    except ValueError:
        return False
    try:
        befriender = request.data['befriender']
        befriender_key = request.data['befriender_key']
    except KeyError:
        return False
    if username + "@" + domain != befriender:
        return False
    if len(befriender_key) != 64:
        return False
    verify_key = VerifyKey(bytes.fromhex(befriender_key))
    try:
        verify_key.verify(signed_data.encode('utf-8'), bytes.fromhex(signature_bytes_hex))
        return True
    except BadSignatureError:
        return False


def authenticate_request_against_known_identities(request, raw_request_body):
    try:
        username, domain, signed_data, signature_bytes_hex = verify_request(request, raw_request_body)
    except ValueError:
        return None
    try:
        author_identity = KnownIdentity.objects.get(username=username, domain=domain)
    except KnownIdentity.DoesNotExist:
        return None
    if author_identity.verify(signed_data, signature_bytes_hex):
        return author_identity
    else:
        return None


def authenticate_request_against_local_users(request, raw_request_body):
    try:
        username, domain, signed_data, signature_bytes_hex = verify_request(request, raw_request_body)
    except ValueError:
        return None
    try:
        author_user = ToolshedUser.objects.get(username=username, domain=domain)
    except ToolshedUser.DoesNotExist:
        return None
    if author_user.public_identity.verify(signed_data, signature_bytes_hex):
        return author_user
    else:
        return None


class SignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return authenticate_request_against_known_identities(
            request, request.body.decode('utf-8')), None


class SignatureAuthenticationLocal(authentication.BaseAuthentication):
    def authenticate(self, request):
        return authenticate_request_against_local_users(
            request, request.body.decode('utf-8')), None
