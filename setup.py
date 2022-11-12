import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="cloudsen12",
    version="0.0.6",
    url="https://github.com/cloudsen12/cloudsen12",
    license="MIT",
    author="Cesar Luis Aybar Camacho",
    author_email="csaybar@gmail.com",
    description="A Python package for use cloudsen12",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",), include=["cloudsen12", "cloudsen12.*"]),
    install_requires=[
        "maskay",
        "pytorch_lightning",
        "segmentation_models_pytorch",
        "gdown",
        "pystac",
        "dill",
        "shapely",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
