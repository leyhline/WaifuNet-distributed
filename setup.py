from setuptools import setup, find_packages


setup(
    name="waifunet-distributed",
    version="0.1",
    description="Small-scale distributed deep learning with TensorFlow",
    url="https://github.com/leyhline/WaifuNet-distributed",
    author="Thomas Leyh",
    author_email="thomas.leyh@mailbox.org",
    packages=find_packages(include=["waifunet"]),
    test_suite="tests"
)