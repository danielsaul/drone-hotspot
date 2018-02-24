from setuptools import setup, find_packages

setup(
    name='drone-control',
    version='0.1.0',
    packages=find_packages(exclude=('tests', 'docs')),
    url='https://github.com/danielsaul/drone-hotspot',
    author='danielsaul',
    author_email='daniel@dansaul.co.uk',
    description='Control program for Drone Hotspot',
    entry_points={
        'console_scripts': ['drone-control = drone_control.main:main']
    }
)
