# Blockchain Security 2Go starter kit Python Library

This package provides basic functions to communicate with Infineon's Blockchain Security 2Go 
starter kit. It abstracts all of the commands available with the starter kit with some simple 
functions. 

To get more information about the starter kit go to https://github.com/Infineon/blockchain.

## Getting Started
To use this library you need some hardware first:
* A smart card from Infineon's Blockchain Security 2Go starter kit 
(see [here](https://www.infineon.com/blockchain) for information about how to get it), and
* a contactless reader to communicate with the contactless smart card. We recommend to use 
a reader that is connected via USB (a list is available at 
[ccid.apdu.fr](https://ccid.apdu.fr/select_readers/?features=contactless)). 

### Install Prerequisites
To use the library you need a Python 3 installation (e.g. from http://python.org or via [Anaconda](https://www.anaconda.com/)). 
The BlockSec2Go library depends on `pyscard` that requires `swig`. To install `swig` follow the guides at https://github.com/LudovicRousseau/pyscard/blob/master/INSTALL.md or follow the hints below. 

On Windows, we recommend to use the chocolately package manager:
* Install the chocolately package manager
* Open a powershell as administrator mode, run
```
$ choco install swig
```
On Linux, run
```
$ sudo apt-get install swig
```
For Mac systems, we recommend to use homebrew
```
$ brew install swig
```

### Install BlockSec2Go

Then, the fastest way to install the library is to get it via pip

    $ pip3 install blocksec2go

Remark: When installing Python 3>=3.4 the installer program `pip` is automatically installed (see https://pip.pypa.io/en/stable/installing/). 

This will install the library, which can be imported as `blocksec2go`.
In addition the `blocksec2go` command will be installed which can be used to communicate with 
the card from the command line.

To find out more, run

    $ blocksec2go --help

The library is tested with Python 3.7.1 and the Identive Cloud 4700 F Dual Interface reader.

## Usage Example
### Command Line Tool
Here is an example of how the command line tool could be used

    $ blocksec2go get_card_info
      PIN is: disabled
	  Card ID (hex): 02058d190004001a002d
	  Version: v1.0

	$ blocksec2go set_pin 1234
	  PUK to unlock card (hex): 5c88ce829a2ed32c

	$ blocksec2go generate_keypair
	  Key ID: 1

	$ blocksec2go get_key_info 1
	  Remaining signatures with card: 999990
      Remaining signatures with key 1: 100000
      Public key (hex, encoded according to SEC1): 0434cfd6b1bb53fc244d4881cf1f0d3b9aee7b6ac28aad8a1648fc514101961b59fa7fc58751d0dc876589e467a63ed1582e240cd18b98d408470679418a647833

	$ blocksec2go generate_signature --pin 1234 1 00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF
	  Remaining signatures with card: 999989
      Remaining signatures with key 1: 99999
      Signature (hex): 3044022049689b91545ba3bc487af7cb7267d19ea4ad8e2e8b093458e06d46837400444702207fe7cd2b6851049afe0f7c4ced0ef35bd9eb5d044c67ed95045b07a10641806c

### Python Library
The command line tool is an abstraction of the Python functions that are delivered by this library. Have a look at the implementation of the commands in [blocksec2go/cli](blocksec2go/cli) to see how the functions are used. 

<!-- Go to the [Blockchain Security 2Go repository](https://github.com/Infineon/BlockchainSecurity2Go-Python-Library) to find examples of how to use the Python library. -->

## Testing

To develop/test, it's best to use virtualenv. It allows for installing packages
in a "private" environment (for details see https://virtualenv.pypa.io/en/latest/)
(commands intended for Windows in bash, small differences for other OS/shell combinations)

    $ virtualenv venv
    $ source ./venv/Scripts/activate
    $ pip install --editable .

You can now test the library as if it would have been installed.
To exit the environment, simply run

    $ deactivate
