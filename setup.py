import platform
from setuptools import setup

setup(
    name = 'qa-aip',
    version = '2.2.17.0',
    packages = [
        'aip',
    ],
    install_requires=[
        'requests',
    ],
    scripts = [
        'bin/aip_client',
    ] if 'Windows' not in platform.system() else [],
    license = 'Apache License',
    author = 'Demon_he',
    author_email = '1319522956@qq.com',
    url = 'https://github.com/Demonhesusheng/QA_System.git',
    description = 'QA AIP SDK',
    keywords = ['QA', 'aip', 'ocr', 'antiporn', 'nlp', 'face', 'kg', 'speech'],
)