import logging
logger = logging.getLogger(__name__)

from smartcard.System import readers
from blocksec2go.comm.card_observer import card_observer
from blocksec2go.comm.pyscard import open_pyscard

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes

def add_callback(connect, disconnect):
    """ Add callbacks

    Adds function callbacks to ``CardObserver`` class

    Args:
        connect (func): Function to call when card gets connected
        disconnect (func): Function to call when card gets disconnected

    Returns:
    Raises:
    """
    card_observer.connect = connect
    card_observer.disconnect = disconnect

def find_reader(reader_name):
    """ Looks for a specific card reader

    Tries to find a card reader with specified name.

    Args:
        reader_name (str): string providing name of reader

    Returns:
        reader:
            :obj:`PyScardReader`: PyScard wrapper object.
            Chooses first reader with specified name if multiple 
            readers are found.

    Raises:
        RuntimeError: No reader found with specified name.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    logger.debug('FIND READER name %s', reader_name)
    r = readers()
    for reader in r:
        if reader_name in str(reader):
            try:
                return open_pyscard(r[r.index(reader)])
            except:
                raise RuntimeError('No card on reader')
    raise RuntimeError('No reader found')

def select_app(reader):
    """ Sends command to select the Blockchain Security2GO application

    Needs to be called after reset to allow for access to
    blockchain commands.

    Returns:
        :obj:`tuple`: (pin_active, card_id, version).
        
        pin_active:
            bool: True if PIN is set on the card
        
        card_id:
            bytes: 10 byte unique card identifier
        
        version:
            str: card firmware version, following
            semantic versioning.
    
    Raises:
        CardError: If card indicates a failure.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    logger.debug('SELECT Blockchain Security 2Go starter kit')
    aid = bytes.fromhex('D2760000041502000100000001')
    r = reader.transceive(b'\x00\xA4\x04\x00', aid).check()

    pin_active = True if r.resp[0] == 1 else False
    card_id = r.resp[1:11]
    version = r.resp[11:].decode('ASCII')
    return (pin_active, card_id, version)

def generate_keypair(reader):
    """ Sends command to generate new keypair

    A new keypair is generated and stored. The ID identifying this
    keypair is returned. A key using the `secp256k1`_ curve is generated.

    Args:
        reader (:obj:): object providing reader communication

    Returns:
        int: ID of the just generated keypair, to be used e.g. for
        future signatures using ``generate_signature``
    
    Raises:
        CardError: If card indicates a failure, e.g. if card is full.
        
        Any exceptions thrown by the reader wrapper are passed through.
    
    .. _secp256k1:
        http://www.secg.org/sec2-v2.pdf
    """
    logger.debug('GENERATE KEYPAIR')
    r = reader.transceive(b'\x00\x02\x00\x00').check()

    key_id = int(r.resp[0])
    logger.debug('generated key %d', key_id)
    return key_id

def get_key_info(reader, key_id):
    """ Sends command to retrieve keypair information

    Args:
        reader (:obj:): object providing reader communication
        key_id (int): key ID as returned by ``generate_keypair``
    
    Returns:
        :obj:`tuple`: (global_counter, counter, key)

        global_counter:
            int: overall remaining signatures for this card
        
        counter:
            int: signatures remaining with key ``key_id``
        
        key:
            bytes: public key, encoded uncompressed as
            point according to `SEC1`_
        
        Uncompressed SEC1 encoding in short means that the key is
        encoded to a 65 byte string. It consists of a 1 byte prefix
        followed by the coordinates (first x then y) with a constant
        length of 32 byte each.
        The prefix is always 0x04, both coordinates are encoded as
        unsigned integers, MSB first (big endian).
    
    Raises:
        CardError: If card indicates a failure, e.g. if ID is invalid.
        
        Any exceptions thrown by the reader wrapper are passed through.
    
    .. _SEC1:
        http://www.secg.org/sec1-v2.pdf
    """
    logger.debug('GET KEY INFO key %d', key_id)
    if key_id < 0 or key_id > 255:
        raise RuntimeError('Invalid key_id: ' + str(key_id))

    header = '0016{:02x}00'.format(key_id)
    r = reader.transceive(bytes.fromhex(header))

    global_counter = int.from_bytes(r.resp[0:4], byteorder='big')
    counter = int.from_bytes(r.resp[4:8], byteorder='big')
    key = r.resp[8:]
    logger.debug('global count %d, count %d, public key %s', global_counter, counter, key.hex())
    return (global_counter, counter, key)

def is_key_valid(reader, key_id):
    """ Validate retrieved keypair information

    Args:
        reader (:obj:): object providing reader communication
        key_id (int): key ID as returned by ``generate_keypair``
    
    Returns:
        key_valid:
            bool: True if key is valid, else false
    
    Raises:
        RuntimeError: Entered key_id is outside of keypair scope.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    logger.debug('IS KEY VALID key %d', key_id)
    if key_id < 0 or key_id > 255:
        raise RuntimeError('Invalid key_id: ' + str(key_id))
    global_counter, counter, key = get_key_info(reader, key_id)
    if(0 == global_counter): return False
    elif(0 == counter): return False
    else: return True

def generate_signature(reader, key_id, hash):
    """ Send command to calculate signature

    Signs a given hash using the specified key. The signature is
    done using the sec256k1 curve, and DER encoded.
    The returned signature is canonical, as described in `BIP 62`_.
    Hashing needs to be done on the PC/terminal side, the card expects
    already hashed data.

    If a PIN is enabled on the card, a PIN session must be in
    progress to use ``encrypted_keyimport``. See ``verify_pin``
    for more information.

    Args:
        reader (:obj:): object providing reader communication
        key_id (int): key ID as returned by ``generate_keypair``
        hash (bytes): 32 byte long hash to sign
    
    Returns:
        :obj:`tuple`: (global_counter, counter, signature)

        global_counter:
            int: overall remaining signatures for this card
        
        counter:
            int: signatures remaining with key ``key_id``
        
        signature:
            bytes: DER encoded signature
    
    Raises:
        CardError: If card indicates a failure, e.g. if ID is invalid.
        
        Any exceptions thrown by the reader wrapper are passed through.

    .. _BIP 62:
        https://github.com/bitcoin/bips/blob/master/bip-0062.mediawiki
    """
    logger.debug('GENERATE SIGNATURE key %d hash %s', key_id, hash.hex())
    if key_id < 0 or key_id > 255:
        raise RuntimeError('Invalid key_id: ' + str(key_id))
    if len(hash) != 32:
        raise RuntimeError('Invalid hash length')

    header = '0018{:02x}00'.format(key_id)
    r = reader.transceive(bytes.fromhex(header), hash).check()

    global_counter = int.from_bytes(r.resp[0:4], byteorder='big')
    counter = int.from_bytes(r.resp[4:8], byteorder='big')
    signature = r.resp[8:]
    logger.debug('global count %d, count %d, signature %s', global_counter, counter, signature.hex())
    return (global_counter, counter, signature)

def verify_signature(key, hash, signature):
    """ Verification command to check signature

    Verifies a signature which is returned by ``generate_signature``
    using a public key and the hashed message. The returned value
    is a True boolean if the signature is verified correctly, but
    returns a InvalidSignature exception if incorrect.

    Args:
        key (bytes): `SEC1`_ encoded uncompressed public key
        hash (bytes): 32 byte long hash which was signed
        signature (bytes): DER encoded signature
    
    Returns:   
        verification:
            boolean: True if signature gets verified correctly
    
    Raises:
        Any exceptions thrown by the cryptography wrapper are passed through.
    """
    logger.debug('VERIFY SIGNATURE public key %s, hash %s, signature %s', key.hex(), hash.hex(), signature.hex())

    public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), key)
    return public_key.verify(signature, hash, ec.ECDSA(utils.Prehashed(hashes.SHA256()))) == None

def encrypted_keyimport(reader, seed):
    """ Sends command to derive key from given seed

    The card will reproducibly generate a key from the
    given seed. This allows the user to backup the seed
    and provides a fallback in case of running our of
    signatures or destruction of the card.
    The key is generated using key derivation as defined
    in `NIST SP 800-108`_ using CMAC-AES256 as defined in
    `NIST SP 800-38B`_.

    If a PIN is enabled on the card, a PIN session must be in
    progress to use ``encrypted_keyimport``. See ``verify_pin``
    for more information.

    Args:
        reader (:obj:): object providing reader communication
        seed (bytes): 16 byte seed to use for key generation
    
    Raises:
        CardError: If card indicates a failure, e.g. for invalid seed length.
        
        Any exceptions thrown by the reader wrapper are passed through.
    
    .. _NIST SP 800-108:
        https://csrc.nist.gov/publications/detail/sp/800-108/final
    .. _NIST SP 800-38B:
        https://csrc.nist.gov/publications/detail/sp/800-38b/final
    """
    logger.debug('GENERATE KEY FROM SEED seed %s', seed.hex())
    if len(seed) != 16:
        raise RuntimeError('Invalid seed length')

    reader.transceive(b'\x00\x20\x00\x00', seed).check()
    logger.debug('success')

def set_pin(reader, pin):
    """ Send command to set a PIN

    Sets a PIN as long as there is no PIN enabled currently.
    Returns the PUK that is needed in the case of lockout
    because of too many incorrect PIN entries.

    Args:
        reader (:obj:): object providing reader communication
        pin (str): PIN to be used, will be used UTF-8 encoded
    
    Returns:
        bytes: PUK value needed for unlock
    
    Raises:
        CardError: If card indicates a failure, e.g. if there is alredy a PIN set.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    logger.debug('SET PIN pin %s', pin)
    r = reader.transceive(b'\x00\x40\x00\x00', pin.encode()).check()

    logger.debug('new puk %s', r.resp.hex())
    return r.resp

def change_pin(reader, current_pin, new_pin):
    """ Send command to modify existing PIN

    Changes the PIN if a PIN is currently enabled.
    Returns a new PUK that is needed in the case of lockout
    because of too many incorrect PIN entries.

    Args:
        reader (:obj:): object providing reader communication
        current_pin (str): current PIN, will be used UTF-8 encoded
        new_pin (str): new PIN to set, will be used UTF-8 encoded
    
    Returns:
        bytes: PUK value needed for unlock
    
    Raises:
        CardError: If card indicates a failure, e.g. if too many incorrect
        PUK entry tries alrady occured and card is locked permanently.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    logger.debug('CHANGE PIN from %s to %s', current_pin, new_pin)
    if len(current_pin.encode()) > 255:
        raise RuntimeError('Invalid length for current PIN')
    if len(new_pin.encode()) > 255:
        raise RuntimeError('Invalid length for new PIN')

    data = bytes([len(current_pin)]) + current_pin.encode()
    data += bytes([len(new_pin)]) + new_pin.encode()

    r = reader.transceive(b'\x00\x42\x00\x00', data).check()
    logger.debug('new puk %s', r.resp.hex())
    return r.resp

def verify_pin(reader, pin):
    """ Sends command to verify PIN and unlock commands

    If the provided PIN is correct, this starts a PIN
    session. An ongoing PIN session allows to use protected
    commands until the next reset/select command (``select_app``).

    Args:
        reader (:obj:): object providing reader communication
        pin (str)
    
    Returns:

    Raises:
        CardError: If card indicates a failure, e.g. if too many incorrect
        PIN entry tries alrady occured and card is locked.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    # TODO fix interface, do not return bool or int depening on success/failure
    logger.debug('VERIFY PIN pin %s', pin)
    r = reader.transceive(b'\x00\x44\x00\x00', pin.encode())

    if r.sw == 0x9000:
        logger.debug('success')
        return True
    if r.sw == 0x6983:
        logger.debug('failed - PIN locked')
        return 0
    if (r.sw & 0xFFF0) == 0x63C0:
        logger.debug('failed, %d tries remaining', r.sw & 0xF)
        return r.sw & 0xF
    r.check()

def unlock_pin(reader, puk):
    """ Send command to unlock PIN using PUK

    If too many incorrect PIN entries occured and the card is locked
    it can be unlocked using the PUK returned while setting the PIN.

    Args:
        reader (:obj:): object providing reader communication
        pin (bytes): as returned from ``set_pin`` or ``change_pin``
    
    Returns:
        ...
    
    Raises:
        CardError: If card indicates a failure, e.g. if too many incorrect
        PIN entry tries alrady occured and card is locked.
        
        Any exceptions thrown by the reader wrapper are passed through.
    """
    # TODO fix interface, do not return bool or int depening on success/failure
    logger.debug('UNLOCK PIN puk %s', puk.hex())
    r = reader.transceive(b'\x00\x46\x00\x00', puk)
    
    if r.sw == 0x9000:
        logger.debug('success')
        return True
    if r.sw == 0x6983:
        logger.debug('failed - card locked')
        return 0
    if (r.sw & 0xFFF0) == 0x63C0:
        logger.debug('failed, %d tries remaining', r.sw & 0xF)
        return r.sw & 0xF
    r.check()
