# Python Library for Infineon's Blockchain Security 2Go Starter Kit 

This package provides basic functions to communicate with Infineon's Blockchain Security 2Go 
starter kit. It abstracts all of the commands available with the starter kit with some simple 
functions. 

To get more information about the starter kit go to [https://github.com/Infineon/blockchain].

## Getting Started
To use this library you need some hardware first:
* A smart card from Infineon's Blockchain Security 2Go starter kit 
(see [here](https://www.infineon.com/blockchain) for information about how to get it), and
* a contactless reader to communicate with the contactless smart card. We recommend to use 
a reader that is connected via USB (a list is available at 
[ccid.apdu.fr](https://ccid.apdu.fr/select_readers/?features=contactless)). 

The fastest way to install the library is to get it via pip
    $ pip install blocksec2go

This will install the library, which can be imported as `blocksec2go`.
In addition the `blocksec2go` command will be installed which can be used to communicate with 
the card from the command line.

To find out more, run

    $ blocksec2go --help

## Usage Example
### Python Library
Go to the (Blockchain Security 2Go repository)[https://github.com/Infineon/Blockchain/pc] to find examples of how to use the Python library.

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
