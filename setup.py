""" Setuptool setup module """
from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="atmega",
    version="0.0.2",    
    description="Provides an API for atmega devices (memory manipulation)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CEA-IM2AG/ATMEGA-API",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    keywords="API, development, FTDI, RS232, USB, Serial",
    author="Sofiane DJERBI, Ny Aina PEDERSEN, Aymes FREZJA, Nour LADHARI, Yanis ACHAICHIA, Amine OTMANE",
    author_email="sofiane.djerbi@etu.univ-grenoble-alpes.fr",
    packages=find_packages(),
    install_requires=["pyserial"],
    test_suite="tests"
)