from setuptools import setup, find_packages

__version__ = "0.1"


setup(
    name="{{ project_name }}",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=["oy", "python-dotenv"],
)
