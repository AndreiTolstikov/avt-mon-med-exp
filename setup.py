
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='avtMonMedExp',
    version='1.0.0',
    description='avtMonMedExp project using Amazon Comprehend Medical with Python3 ',
    long_description=readme,
    author='A.V.T. Software (Sole Proprietorship Vita Tolstikova: Andrei Tolstikov, Vita Tolstikova)',
    author_email='support@software.avt.dn.ua',
    url='https://github.com/SP-Vita-Tolstikova/avt-mon-med-exp',
    license=license,
    packages=find_packages()
)
