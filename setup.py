from setuptools import find_packages, setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="freegpt",
    version="0.0.1",
    description="Using chatgpt from python without login",
    author="maguroshouta",
    packages=find_packages(),
    license="MIT",
    install_requires=[_requires_from_file("requirements.txt")],
)
