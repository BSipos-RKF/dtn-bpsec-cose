import os
from setuptools import setup, find_packages

setup(
    # Basic info
    name='ietf-dtn-bpsec-cose-demo',
    version='0.0',
    author='Brian Sipos',
    author_email='bsipos@rkf-eng.com',
    url='https://github.com/BSipos-RKF/dtn-bpsec-cose/',
    description='Examples of COSE/BPSEC operations.',
    long_description='''\
''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License (LGPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],

    # Packages and depencies
    package_dir={
        '': 'src',
    },
    packages=find_packages(where='src'),
    install_requires=[
        'scapy >=2.4',
        'cbor2 >=4.1,<4.2',
        'PyGObject >=3.34', # glib integration
    ],
    extras_require={},

    # Data files
    package_data={},

    # Scripts
    entry_points={
        'console_scripts': [
            'example_encrypt0 = bpsec_cose.example_encrypt0:main',
        ],
    },

    # Other configurations
    zip_safe=True,
    platforms='any',
)
