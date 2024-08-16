#!/usr/bin/python3
# coding: utf-8

from setuptools import setup, find_packages


setup(name='pytrx',
      version='1.0',
      description='Python Tron library',
      keywords='ethereum',
      url='https://github.com/bitaps-com/pytrx',
      author='Nadezhda Karpova',
      author_email='nadyka@bitaps.com',
      license='GPL-3.0',
      packages=find_packages(),
      install_requires=['py-ecc==1.4.2','rlp==0.6.0','coincurve','pysha3==1.0.2', 'requests==2.32.3', 'base58==2.1.1'],
      include_package_data=True,
      package_data={
          'pytrx': ['bip39_word_list/*.txt'],
      },
      zip_safe=False)