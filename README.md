# Blockchain Security 2Go starter kit Python library

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
    $ pip install blocks2go

This will install the library, which can be imported as `blocks2go`.
In addition the `blocks2go` command will be installed which can be used to communicate with 
the card from the command line.

## Usage Example
<!-- TODO -->

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



<!--
To use from the IFX network just install the package via pip

    $ pip install git+https://bitbucket.vih.infineon.com/scm/~wallnean/python-blocks2go.git

This will install the library, which can be imported as `blocks2go`.
In addition the `bc2go` command will be installed which can be used to communicate
with the card from the command line.
To find out more, run

    $ bc2go --help
-->