from distutils.core import setup

setup(
    name='SoSAT',
    version='0.0.1',
    author='Matthias Springer, Dominik Moritz',
    author_email='matthias.springer@student.hpi.uni-potsdam.de, dominik.moritz@student.hpi.uni-potsdam.de',
    packages=['sosat', 'sosat.test'],
    scripts=[],
    url='https://github.com/domoritz/SoSAT',
    license='LICENSE.txt',
    description='SAT solver',
    long_description=open('README.md').read(),
    install_requires=[
        "nose"
    ],
)
