from setuptools import find_packages, setup
from typing import List


def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.replace('\n', '') for r in requirements]

        if '-e .' in requirements:
            requirements.remove('-e .')

        return requirements

setup(
    name='medcost',
    version='0.0.0',
    author='saraimdad',
    author_email='saraimdad12@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)