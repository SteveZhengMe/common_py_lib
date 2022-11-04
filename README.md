# Python libraries #

![Release PyPi](https://github.com/SteveZhengMe/common_py_lib/actions/workflows/release.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/common-py-lib.svg)](https://badge.fury.io/py/common-py-lib)

## Command line ##

- Build a package: `python setup.py sdist bdist_wheel`
- Install to AWS CodeArtifact: `./install_AWS_CodeArtifacts.sh [Domain Name] [Repo Name] [AWS profile name if has multiple]`
- Install to PyPi: `./install_pypi.sh [PyPi username] [PyPi password]`
- Use the package (You need to login to the AWS CodeArtifacts using CLI): `pip install common-py-lib`

## Change Notes

- 2022-11-02 (v1.4): Initial release with logging and aws services support
- 2022-11-04 (v1.5.0): Easy maintenance of the Version