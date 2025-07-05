from setuptools import setup

with open('requirements.txt', mode='r', encoding='utf-8') as requirements:
    install_requirements = requirements.read().splitlines()

with open('README.md', mode='r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='sentence_splitter',
    version='0.1.0',
    author='wangzejun',
    author_email='wangzejunscut@126.com',
    description='Split Chinese text and English text to sentences.',
    long_description=long_description,
    url='https://github.com/zejunwang1/sentence-splitter',
    license="LGPLv3",
    install_requires=install_requirements,
    packages=['sentence_splitter'],
    package_dir={'sentence_splitter': 'sentence_splitter'},
    package_data={'sentence_splitter': [
        'non_breaking_prefixes/*.txt',
    ]},
    include_package_data=True,
    python_requires=">=3.5"
)
