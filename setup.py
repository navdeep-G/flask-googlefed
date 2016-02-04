# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Flask-GoogleFed',
    version='0.1',
    url='https://github.com/kennethreitz/flask-googlefed',
    license='BSD',
    author='Kennneth Reitz',
    author_email='me@kennethreitz.com',
    description='Google Federated Logins for Flask.',
    long_description=open('README.rst', 'r').read(),
    py_modules=['flask_googlefed'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-OpenID==1.1.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
