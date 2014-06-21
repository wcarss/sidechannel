from setuptools import setup
from pip.req import parse_requirements


# pip requirements parsing code taken from http://stackoverflow.com/a/16624700
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='sidechannel',
    version='0.1dev',
    long_description=open('README.md').read(),
    install_requires=reqs
)
