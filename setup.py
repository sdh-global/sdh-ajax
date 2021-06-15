#!/usr/bin/env python
from setuptools import setup, find_packages

import os

version = '1.0.11'

setup(
    name='sdh.ajax',
    namespace_packages=['sdh'],
    packages=find_packages('src'),
    package_data={'': ['*.*']},
    package_dir={'': 'src'},
    entry_points={},
    eager_resources=['sdh'],
    version=version,
    install_requires=['Django>=2.2', ],
    license='BSD License',
    include_package_data=True,
    zip_safe=False,
    author='Viacheslav Vic Bukhantsov',
    author_email='vic@sdh.com.ua',
    platforms=['OS Independent'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'],
    description='Django ajax helper',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://bitbucket.org/sdh-llc/sdh-ajax',
)
