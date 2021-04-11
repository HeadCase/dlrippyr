from setuptools import setup

setup(
    name='dlrippyr',
    version='0.1.0',
    py_modules=['dlrippyr'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        dlrippyr=dlrippyr:cli
    ''',
)
