from setuptools import setup
from setuptools import find_packages
import sys
import os.path

if sys.version_info < (3, 6):
    raise RuntimeError("Karuba requires Python 3.6")

# Don't import copydetection module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "copydetection"))

from version import VERSION  # noqa: E402


setup(
    name="karuba",
    version=VERSION,
    description="Karuba board game",
    url="",
    author="Lowik Chanussot",
    author_email="lowikchanussot@gmail.com",
    install_requires=["pygame", "attrs"],
    license="",
    packages=find_packages(exclude=("configs", "tests")),
)
