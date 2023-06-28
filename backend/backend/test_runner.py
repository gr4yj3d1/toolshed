from django.conf import settings
from django.test.runner import DiscoverRunner


class FastTestRunner(DiscoverRunner):
    def setup_test_environment(self):
        super(FastTestRunner, self).setup_test_environment()
        # Don't write files
        settings.STORAGES = {
            'default': {
                'BACKEND': 'django.core.files.storage.InMemoryStorage',
                'OPTIONS': {
                    'base_url': '/media/',
                    'location': '',
                },
            },
        }
        # Bonus: Use a faster password hasher. This REALLY helps.
        settings.PASSWORD_HASHERS = (
            'django.contrib.auth.hashers.MD5PasswordHasher',
        )
