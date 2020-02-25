import sys
from shutil import rmtree
from setuptools import setup, find_packages

if sys.argv[:2] == ["setup.py", "bdist_wheel"]:
    # Remove previous build dir when creating a wheel build, since if files
    # have been removed from the project, they'll still be cached in the build
    # dir and end up as part of the build, which is unexpected
    try:
        rmtree("build")
    except:
        pass


version = {}

with open("gnupg_mails/__init__.py") as fp:
    exec(fp.read(), version)


setup(
    name="django-gnupg-mails",
    version=version['__version__'],
    author="Jan Dittberner",
    author_email="jan@dittberner.info",
    description=(
        "A Django reusable app providing the ability to send PGP/MIME signed "
        "multipart emails."
    ),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/jandd/django-gnupg-mails",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["Django", "python-gnupg", "sphinx-me"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Topic :: Communications :: Email",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.5',
)
