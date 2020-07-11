from setuptools import setup, find_namespace_packages

setup(
    name="Card Deck",
    version="0.1",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
)

