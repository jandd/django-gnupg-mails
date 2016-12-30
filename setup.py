import sys
from shutil import rmtree
from setuptools import setup, find_packages


if sys.argv[:2] == ['setup.py', 'bdist_wheel']:
    # Remove previous build dir when creating a wheel build, since if files
    # have been removed from the project, they'll still be cached in the build
    # dir and end up as part of the build, which is unexpected
    try:
        rmtree('build')
    except:
        pass


setup(
    name = "django-gnupg-mails",
    version = __import__("gnupg_mails").__version__,
    author = "Jan Dittberner",
    author_email = "jan@dittberner.info",
    description = (
        "A Django reusable app providing the ability to send PGP/MIME signed "
        "multipart emails."
    ),
    long_description = open("README.rst").read(),
    url = "https://github.com/jandd/django-gnupg-mails",
    packages = find_packages(),
    zip_safe = False,
    include_package_data = True,
    install_requires = ['python-gnupg', 'sphinx-me'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Communications :: Email',
        'Topic :: Security :: Cryptography',
    ]
)
