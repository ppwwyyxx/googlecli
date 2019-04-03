#-*- coding: utf-8 -*-
#File:


from setuptools import setup
kwargs = dict(
  name = 'googlecli',
  version = '0.1',
  description = 'Command line google search',
  author = 'Yuxin Wu',
  url = 'https://github.com/ppwwyyxx/googlecli',
  keywords = ['Utility'],
  py_modules = ['googlecli'],
  packages = [],
  entry_points={
      'console_scripts': ['google = googlecli:main']
  },
  install_requires=['beautifulsoup4', 'six']
)
setup(**kwargs)
