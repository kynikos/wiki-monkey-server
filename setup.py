from setuptools import setup, find_packages

setup(
    name='wiki-monkey',
    version='5.0.0',
    description="Wiki Monkey - MediaWiki bot and editor-assistant user script.",
    long_description="Wiki Monkey - MediaWiki (ArchWiki-optimized) bot and "
        "editor-assistant user script (server-enabled version).",
    url='https://github.com/kynikos/wiki-monkey',
    author='Dario Giovannetti',
    author_email='dev@dariogiovannetti.net',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Database Engines/Servers',
    ],
    python_requires='>=3',
    install_requires=(
        # Do not pin dependencies to specific versions in install_requires
        # https://packaging.python.org/discussions/install-requires-vs-requirements
        # Keep in sync with requirements.txt and PKGBUILD
        'apispec',
        'configfile',
        'Flask-Cors',
        'flask-marshmallow',
        'Flask-Migrate',
        'flask-restinpeace',
        'Flask-SQLAlchemy',
        'marshmallow-sqlalchemy',
        # pyOpenSSL is required only if using an ad-hoc certificate
        # Optional dependencies shouldn't be added to install_requires
        # 'pyOpenSSL',
        'pyxdg',
    ),
    keywords='wikimonkey wiki-monkey wiki mediawiki archwiki wikipedia',
    packages=find_packages(exclude=('contrib', 'docs', 'tests')),
    entry_points={
        'console_scripts': (
            'wiki-monkey = wiki_monkey.main:main',
            'wiki-monkey-gencert = wiki_monkey.gencert:main',
        ),
    },
    package_data={
        'wiki_monkey': ['migrations/*', 'migrations/**/*'],
    },
    data_files=[
        ('/usr/share/wiki-monkey/', (
            'wiki-monkey/dist/WikiMonkey-ArchWiki.js',
            'wiki-monkey/dist/WikiMonkey-ArchWiki.min.js',
            'wiki-monkey/dist/WikiMonkey-Wikipedia.js',
            'wiki-monkey/dist/WikiMonkey-Wikipedia.min.js',
        )),
        ('/usr/lib/systemd/user/', (
            # "-" has a special meaning in systemd unit names
            'auxiliary/wiki_monkey.service',
            'auxiliary/wiki_monkey@.service',
        )),
    ],
)
