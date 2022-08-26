import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

with open(os.path.join(here, "LONG_DESCRIPTION.rst"), "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="smartmine",
    description="Python bindings for the Smartmine API",
    version="0.2.2",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Smartmine",
    author_email="info@smartmine.net",
    url="https://smartmine.net",
    license="MIT",
    keywords="smartmine api",
    package_dir={"": "."},
    packages=find_packages(exclude=["tests", "tests.*", "api_demo.py"]),
    zip_safe=False,
    install_requires=["requests", "tqdm", "Pillow"],
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["wheel"],
)
