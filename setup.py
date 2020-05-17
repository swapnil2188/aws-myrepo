from setuptools import setup

setup(
    name='aws-tools',
    version='0.1',
    author="Swapnil Shevate",
    author_email="swapnil2188@gmail.com",
    description="aws-tools are set of scripts to manage your EC2 Instances",
    license="GPLv3+",
    packages=['scripts'],
    url="https://github.com/swapnil2188/aws-myrepo/tree/master/scripts",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        scripts=scripts.swap2:cli
    ''',
)
