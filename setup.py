import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metric4coref",
    version="0.0.2",
    author="LowinLi",
    author_email="lowinli@outlook.com",
    description="metric for coreference resolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LowinLi/metric4coref",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy>=1.18", "scipy>=1.4.1"],
    keywords="coreference resolution metric",
)
