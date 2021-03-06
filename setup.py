from setuptools import setup

setup(
    name='sosat',
    version='0.0.1',
    author='Matthias Springer, Dominik Moritz',
    author_email='matthias.springer@student.hpi.uni-potsdam.de, dominik.moritz@student.hpi.uni-potsdam.de',
    packages=['', 'sosat', 'sosat.annealing', 'sosat.ant', 'sosat.genetic'],
    scripts=[],
    url='https://github.com/domoritz/SoSAT',
    license='LICENSE.txt',
    description='SAT solver',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy>=1.7',
        'bottleneck'
    ],
    entry_points={
        'console_scripts': [
            'sosat = main:main'
        ],
    },
)
