import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bank_transactions",
    version="0.0.1",
    author="Daniel Bibik",
    author_email="work.danbibik@gmail.com",
    description="REST API implementation of the simple bank app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Boring-Mind/bank-transactions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
