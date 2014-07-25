from distutils.core import setup

setup(
    name='BattleQuip',
    version='0.1.0',
    author='Casey Chance',
    author_email='caseyjchance@gmail.com',
    packages=['battlequip', 'battlequip.test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/BattleQuip/',
    license='LICENSE.txt',
    description='A chatty Battleship client.',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
