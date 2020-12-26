import os
from setuptools import setup, find_packages

# read the contents of your README file
directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md')) as fl:
    long_description = fl.read()

setup(
    name = "OpenPIVToolkit",
    version ='0.2.8',
    packages=find_packages(),
    include_package_data=True,
    description='Toolkit for PIV Processing and Post-Processing',
    url="https://github.com/pouya-m/openpiv-toolkit",
    author="Pouya Mohtat",
    author_email="pouya.m67@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=[
        'setuptools'
    ],
    install_requires=[
        'numpy',            
        'imageio',
        'matplotlib>=3',
        'scikit-image',
        'scipy',
        'PySide2'
    ],
    classifiers = [
        # PyPI-specific version type. The number specified here is a magic constant
        # with no relation to this application's version numbering scheme. *sigh*
        'Development Status :: 4 - Beta',

        # Sublist of all supported Python versions.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        # Sublist of all supported platforms and environments.
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',

        # Miscellaneous metadata.
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
    ]
)
