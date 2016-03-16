from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='pandas-validation',
    version=__import__('pandasvalidation').__version__,
    description=(
        'A Python package for validating data with pandas'),
    long_description = open(
        join(dirname(__file__), 'README.rst'), encoding='utf-8').read(),
    packages=find_packages(exclude=['docs', 'tests*']),
    py_modules=['pandasvalidation'],
    install_requires=['pandas>=0.16', 'numpy'],
    extras_require={'test': ['coverage', 'pytest', 'pytest-cov']},
    author='Markus Englund',
    author_email='jan.markus.englund@gmail.com',
    url='https://github.com/jmenglund/pandas-validation',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',],
    keywords=['pandas', 'validation'],
)