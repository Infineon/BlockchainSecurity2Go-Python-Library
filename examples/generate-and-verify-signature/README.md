# Generate and verify a signature

This examples shows you to generate a signature on the Blockchain Security 2Go card and how to verify a signature using the blocksec2go library.

The contents of `get_reader()` and `activate_card(reader)` have already been covered in the example [get-card-info](../get-card-info) and the content of `get_public_key(key_id)` in the example [get_key_info](../get-key-info). Please reference those earlier examples if something is unclear in these functions.

To use the `generate_signature(reader, key_id, hash)` command we first need a hashed message that should be signed using the card. In the example we used "Hello World!" as our message and hashed it using the SHA256 algorithm:

    hash_object = hashlib.sha256(b'Hello World!')
    hash = hash_object.digest()

It is important that we leave the hashed message in bytes since this is the format the card accepts.

Next, we need a keypair which will be used to sign the hashed message. Please be sure to validate the keypair using the function `is_key_valid(reader, key_id)` since otherwise there is a chance that there is no private key for the signing process.

After a hashed message and a valid keypair exist we can proceed to actually generate a signature:

    global_counter, counter, signature = blocksec2go.generate_signature(reader, key_id, hash)

The returned values `global_counter` and `counter` are the same as with the command `get_key_info(reader, key_id)`. The `signature` varibale is the signed hash message in the DER encoded format. For more information on this please check the [Blockchain Security 2Go user manual](https://github.com/Infineon/Blockchain/blob/master/doc/BlockchainSecurity2Go_UserManual.pdf) under paragraph *4.3.2.4 GENERATE SIGNATURE* &rightarrow; *Table 24 ASN.1 DER Signature Encoding Details*.

The verification of signatures is also possible using the blocksec2go library by using the function `verify_signature(public_key, hash, signature)`. To verify, you will need the hashed message and the public key which correspond to the signed message:

    print('Is signature correct?', blocksec2go.verify_signature(public_key, hash, signature))

This command returns a `True` boolean if the signature is correct. If the signature does not correspond to the given public key and hash then a `InvalidSignature` exception will be called. It is important to note that this exception is not part of the blocksec2go library itself, but is passed on by the cryptography library:

    import cryptography.exceptions as crypto_except
    ...
    except crypto_except.InvalidSignature:
        print('Verification failed!')