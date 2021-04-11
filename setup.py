from setuptools import setup

setup(
    name='dlrippyr',
    version='0.0.1',
    py_modules=['dlrippyr'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        dlrippyr=dlrippyr:cli
    ''',
)
