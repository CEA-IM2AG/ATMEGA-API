from setuptools import setup

setup(
    name="atmega",
    version="0.0.1",    
    description="Provides an API for atmega devices (memory manipulation)",
    url="https://github.com/CEA-IM2AG/ATMEGA-API",
    author="Sofiane DJERBI, Ny Aina PEDERSEN, Aymes FREZJA, Nour LADHARI, Yanis ACHAICHIA, Amine OTMANE",
    author_email="sofiane.djerbi@etu.univ-grenoble-alpes.fr",
    packages=["atmega"],
    install_requires=["pyserial"]
)