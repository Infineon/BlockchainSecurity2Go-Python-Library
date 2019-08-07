# Generating new keypairs and getting key information

This example shows you how to generate new keypairs (public and private keys) and how to recieve important information such as how many signatures the card/key has left or the uncompressed public key corresponding to a specific keyslot.

The contents of `get_reader()` and `activate_card(reader)` have already been covered in the previous example [get-card-info](../get-card-info). Please reference that example if something is unclear in these functions.

By default the Blockchain Security 2Go card does not come with any preloaded keys. If this is your first time using the card you have to tell it to generate a keypair using the command `generate_keypair(reader)`:

    key_id = blocksec2go.generate_keypair(reader)

This function returns the keyslot on which the keypair was generated.

One of the features of the Blockchain Security 2Go card is that it can store up to 255 keypairs. To get access to a specific keypair you can use the function `get_key_info(reader, key_id)`:

    global_counter, counter, key = blocksec2go.get_key_info(reader, key_id)

This function returns you a tuple:  
The `global_counter` and `counter` variables show how many signatures the card/key have left.  
The variable `key` is the Sec1 encoded uncompressed public key of the keypair.

An example output may look like this:

    Found the specified reader and a Blockchain Security 2Go card
    Do you want to create a new Keypair? ("Yes" or "No")
    Yes
    Keypair generated on slot 1
    Get information on which key? (Number between 0-255 only)
    1
    Remaining signatures with card: 1000000
    Remaining signatures with key 1: 100000
    Public key (hex, encoded according to SEC1):    04f70b746ef8c0a6cb23a0ea80c0ccdbb126651299c563cd5896f115c19f1530c32a01ace42842c81142baae62bd142248eadb1bd4fbafbb065c82d5b3c8743990

## Warning
Please be sure that the connection between the card and the reader does not get interrupted during the process of generating a new keypair because disturbances during this step can render that keyslot obsolete. If this happens or if a keypair on that slot was not generated yet the command `get_key_info(reader, key_id)` will return 0 remaining signatures on the card/key and the public key will be blank:

    Remaining signatures with card: 0
    Remaining signatures with key 1: 0
    Public key (hex, encoded according to SEC1):