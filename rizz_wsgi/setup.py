#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os


from setuptools import find_packages, setup


# package meta-data
NAME = "rizz_wsgi"
DESCRIPTION = "Rizz WSGI Python Framework for science purposes."
EMAIL = "kiuraalex@gmail.com"
AUTHOR = "Alex Kiura"
REQUIRES_PYTHON = ">=3.10.0"
VERSION = "0.0.2"


REQUIRED_PACKAGES = [
    "Jinja2==3.1.2",
    "parse==1.19.1",
    "requests==2.31.0",
    "requests-wsgi-adapter==0.4.1",
    "WebOb==1.8.7",
    "whitenoise==6.5.0"
]

here = os.path.abspath(os.path.dirname(__file__))


# load readme
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("_", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["test_*"]),
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    setup_requires=["wheel"],
)
