from setuptools import setup, find_packages

VERSION = '1.0.0'

setup (
    name = 'django-purr',
    version = VERSION,
    description = '**TESTING** "category" code; see `README.md` for more info.',
    author = 'Micky Hulse',
    author_email = 'micky@hulse.me',
    maintainer = 'Micky Hulse',
    maintainer_email = 'micky@hulse.me',
    url = 'https://github.com/mhulse/django-purr',
    license = 'http://www.apache.org/licenses/LICENSE-2.0',
    platforms = ['any'],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)