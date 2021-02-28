import os
import shutil
import sys

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 3.6.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of tf_vacation_manager requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install tf_vacation_manager
This will install the latest version of tf_vacation_manager which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of tf_vacation_manager:
    $ python -m pip install "tf_vacation_manager<2"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

EXCLUDE_FROM_PACKAGES = []


# Dynamically calculate the version based on tf_vacation_manager.VERSION.
version = __import__('tf_vacation_manager.src.Config').src.Config.Config.module_version


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


shutil.copyfile('tf_vacation_manager/command_line',
                'tf_vacation_manager/tf_vacation_manager')

setup(
    name='tf_vacation_manager',
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/trigrab/tf-vacation-manager/',
    author='Trigrab',
    author_email='trigrab@gmail.com',
    description=('A vacation-manager for tf'),
    long_description=read('README.md'),
    license='GPL-3',
    packages=['tf_vacation_manager',
              'tf_vacation_manager/src'],
    include_package_data=True,
    scripts=['tf_vacation_manager/tf_vacation_manager'],
    entry_points = {
		'gui_scripts': ['tf_vacation_manager=tf_vacation_manager.TFVacationManager:TFVacationManager'],
	},
    install_requires=['Jinja2', 'python-dateutil', 'paramiko', 'scp', 'pyyaml', 'cryptography'],
    zip_safe=True,
    project_urls={
        'Source': 'https://github.com/trigrab/tf-vacation-manager',
    },
)
