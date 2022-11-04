import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

# read requirements.txt as a list
with open('requirements.txt', "r", encoding='utf-8') as f:
    requirements = f.read().splitlines()

version = "1.5.0"

setuptools.setup(
    name="common-py-lib",
    version=version,
    license="MIT",
    author="Steve Zheng",
    author_email="steve.zheng@gmail.com",
    description="Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(exclude=['tests','docs']),
    install_requires=requirements,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)