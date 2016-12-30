from tempfile import mkdtemp

tempdir = mkdtemp()

GNUPG_HOMEDIR = tempdir
INSTALLED_APPS = []
SECRET_KEY = 'testkey'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
