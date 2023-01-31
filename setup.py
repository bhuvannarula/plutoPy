from setuptools import setup

setup(
    name='plutoPy',
    url='https://github.com/bhuvannarula/plutoPy',
    author='Inter IIT',
    author_email='bhuvannarula8@gmail.com',
    packages=['plutopy'],
    package_data={
        '': ['*.py']
    },
    install_requires=[],
    version='1.1',
    license='MIT',
    description='A Python Wrapper for Controlling Pluto Drone',
    #long_description=open('README.md').read(),
)