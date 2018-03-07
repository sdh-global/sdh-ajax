#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os

setup(
    name='sdh.ajax',
    namespace_packages=['sdh'],
    packages=find_packages('src'),
    package_data={'': ['*.*']},
    package_dir={'': 'src'},
    entry_points={},
    eager_resources=['sdh'],
    version='1.0.2',
    install_requires=['Django>=1.5', ],
    license='BSD License',
    include_package_data=True,
    zip_safe=False,
    author='Viacheslav Vic Bukhantsov',
    author_email='vic@sdh.com.ua',
    platforms=['OS Independent'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'],
    description='Django ajax helper',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://bitbucket.org/sdh-llc/sdh-ajax',
)
