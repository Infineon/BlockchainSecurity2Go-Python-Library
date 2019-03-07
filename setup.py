from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
  long_description = fh.read()

setup(
  name='blockchain-security-2go-starterkit',
  version='1.0',
  author='Infineon Technologies AG',
  author_email='blockchain@infineon.com',
  description='Allow for communication with Infineon\'s Blockchain Security 2Go starter kit',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='http://github.com/Infineon/PyBlockSec2Go',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'pyscard'
  ],
  entry_points={
    'console_scripts': [
      'blocksec2go = blocksec2go.cli.main:main',
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  zip_safe=False
)