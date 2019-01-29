import logging

logger = logging.getLogger(__name__)

def select_app(reader):
    logger.debug('SELECT Blockchain Security2GO Starterkit')
    aid = bytes.fromhex('D2760000041502000100000001')
    r = reader.transceive(b'\x00\xA4\x04\x00', aid).check()

    pin_active = True if r.resp[0] == 1 else False
    card_id = r.resp[1:11]
    version = r.resp[11:].decode('ASCII')
    return (pin_active, card_id, version)

def generate_keypair(reader):
    logger.debug('GENERATE KEYPAIR')
    r = reader.transceive(b'\x00\x02\x00\x00').check()

    key_id = int(r.resp[0])
    logger.debug('generated key %d', key_id)
    return key_id

def get_key_info(reader, key_id):
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

def generate_signature(reader, key_id, hash):
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

def generate_key_from_seed(reader, seed):
    logger.debug('GENERATE KEY FROM SEED seed %s', seed.hex())
    if len(seed) != 16:
        raise RuntimeError('Invalid seed length')

    reader.transceive(b'\x00\x20\x00\x00', seed).check()
    logger.debug('success')

def set_pin(reader, pin):
    logger.debug('SET PIN pin %s', pin)
    r = reader.transceive(b'\x00\x40\x00\x00', pin.encode()).check()

    logger.debug('new puk %s', r.resp.hex())
    return r.resp

def change_pin(reader, current_pin, new_pin):
    logger.debug('CHANGE PIN from %s to %s', current_pin, new_pin)
    if len(current_pin) > 255:
        raise RuntimeError('Invalid length for current PIN')
    if len(new_pin) > 255:
        raise RuntimeError('Invalid length for new PIN')

    data = bytes([len(current_pin)]) + current_pin.encode()
    data += bytes([len(new_pin)]) + new_pin.encode()

    r = reader.transceive(b'\x00\x42\x00\x00', data).check()
    logger.debug('new puk %s', r.resp.hex())
    return r.resp

def verify_pin(reader, pin):
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
