"""
This library allows the user to communicate with the
Infineon Blockchain Security2GO Starterkit through python
or using a command line tool.

Command Line:
    The command line tool installed is called ``blocks2go``.
    It is built as a binary with subcommands for the individual
    commands to send to the card.
    To see the supported commands, run:

        $ blocks2go -h
    
    Help for individual commands can be seen by running

        $ blocks2go <command> -h
  
Library usage:
    To interact with the library, an object to communicate with
    the reader is needed. The library includes a wrapper for PC/SC
    devices (using PyScard), for different readers custom wrappers
    must be implemented.

    All supported commands can then be sent using the functions
    from the ``blocks2go.commands`` module.
"""
from blocks2go.commands import *
from blocks2go.comm import *