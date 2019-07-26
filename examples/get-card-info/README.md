# Getting basic card information example

This example shows you how with just a few lines of code you can get the basic card information of your Blockchain Security 2Go card.

First the main blocksec2go library will be imported, since it provides us with an easy way to talk with the card reader and more importantly with the card itself:

    import blocksec2go

Before we can actually communicate with the card we need to find a card reader with a smartcard connected to it. This can be done by using the command `find_reader('name of card reader')`.

If you are unsure what the name of your card reader is, use the command `blocksec2go list_readers` in your cli. Keep in mind that the exact name of the reader can vary across platforms so try keeping the name you enter in the function as simple as possible so it can also be recognised on another platforms too.

For this example the card reader uTrust 3700 F by the company Identiv was used:

    reader_name = 'Identiv uTrust 3700 F'
    ...
    reader = blocksec2go.find_reader(reader_name)

This function returns us the reader as an object to be used with other commands from the blocksec2go library.

The command `select_app(reader)` has to be used in every application that tries to communicate with the Blockchain Security 2Go card because it activates all the Blockchain commands on the card. It also simultaneously returns us some basic information about the card in form of a tuple:

    pin_active, card_id, version = blocksec2go.select_app(reader)

The bool `pin_active` that tells us if the card is locked with a PIN code.  
The variable `card_id` is a unique card identifier which corresponds to that specific Blockchain Security 2Go card.  
The string `version` shows the card firmware version.

Before you run the example script on your machine make sure to replace the string from `reader_name` with the name of your card reader. Also make sure that everything is connected and the Blockchain Security 2Go card is placed properly on the reader.

Your output should look something like:

    Found the specified reader and a Blockchain Security 2Go card!
    Is PIN enabled? False
    Card ID (hex): 02090c2900020027000c
    Version: v1.0
