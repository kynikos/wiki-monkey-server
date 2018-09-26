from setuptools import setup, find_packages

setup(
    name='wiki-snake',
    version='0.1.0',
    description=("Wiki Monkey's server."),
    long_description=("Wiki Monkey's server."),
    url='https://github.com/kynikos/wiki-snake',
    author='Dario Giovannetti',
    author_email='dev@dariogiovannetti.net',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Database Engines/Servers',
    ],
    keywords='flask rest restful api marshal marshmallow',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
