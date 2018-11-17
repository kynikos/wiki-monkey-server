from setuptools import setup, find_packages

setup(
    name='wiki-snake',
    version='0.1.0',
    description="Wiki Monkey's database server.",
    long_description="Wiki Monkey's database server.",
    url='https://github.com/kynikos/wiki-snake',
    author='Dario Giovannetti',
    author_email='dev@dariogiovannetti.net',
    license='GPLv3+',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Database Engines/Servers',
    ),
    python_requires='>=3',
    install_requires=(
        # Do not pin dependencies to specific versions in install_requires
        # https://packaging.python.org/discussions/install-requires-vs-requirements
        # Keep in sync with requirements.txt
        'apispec',
        'configfile',
        'Flask-Cors',
        'flask-marshmallow',
        'Flask-Migrate',
        'flask-restinpeace',
        'Flask-SQLAlchemy',
        'marshmallow-sqlalchemy',
        'pyxdg',
    ),
    keywords='wikimonkey wiki-monkey wiki mediawiki archwiki wikipedia',
    packages=find_packages(exclude=('contrib', 'docs', 'tests')),
    entry_points={
        'console_scripts': (
            # Use wiki-monkey, not wiki-snake, since that's the application
            # that users want to use after all
            # TODO: Maybe just rename the whole project as wiki-monkey-server
            'wiki-monkey = wiki_snake.main',
            'wiki-monkey-gencert = wiki_snake.gencert',
        ),
    },
    data_files=[
        # Relative paths are put inside the installation folder
        ('srv/static/', ('wiki-monkey/dist/*.js')),
        # "-" has a special meaning in systemd unit names
        ('/usr/lib/systemd/user/', (
            'auxiliary/wiki_monkey.service',
            'auxiliary/wiki_monkey@.service',
        )),
    ],
)
