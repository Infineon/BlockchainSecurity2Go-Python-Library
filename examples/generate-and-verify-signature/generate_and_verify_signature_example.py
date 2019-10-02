import blocksec2go
import hashlib
import cryptography.exceptions as crypto_except

def get_reader():
  reader = None
  reader_name = 'Identiv uTrust 3700 F'
  while(reader == None):
    try:
      reader = blocksec2go.find_reader(reader_name)
      print('Found the specified reader and a card!', end='\r')
    except Exception as details:
      if('No reader found' == str(details)):
        print('No card reader found!     ', end='\r')
      elif('No card on reader' == str(details)):
        print('Found reader, but no card!', end='\r')
      else:
        print('ERROR: ' + str(details))
        raise SystemExit
  return reader

def activate_card(reader):
  try:
    blocksec2go.select_app(reader)
    print('Found the specified reader and a Blockchain Security 2Go card!')
  except Exception as details:
    print('ERROR: ' + str(details))
    raise SystemExit

def get_public_key(reader, key_id):
  try:
    if(blocksec2go.is_key_valid(reader, key_id)):
      global_counter, counter, key = blocksec2go.get_key_info(reader, key_id)
      print('Public key (hex, encoded according to SEC1): ' + key.hex())
      return key
    else:
      raise RuntimeError('Key_id is invalid!')
  except Exception as details:
    print('ERROR: ' + str(details))
    raise SystemExit

if('__main__' == __name__):
  reader = get_reader()
  activate_card(reader)

  hash_object = hashlib.sha256(b'Hello World!')
  hash = hash_object.digest()
  print('Hashed message:', hash.hex())

  key_id = int(input('Which key would you like to use? (Numbers 1 - 255 only!)\n'))
  public_key = get_public_key(reader, key_id)

  try:
    global_counter, counter, signature = blocksec2go.generate_signature(reader, key_id, hash)
    print('Remaining signatures with card: ', global_counter)
    print('Remaining signatures with key 1: ', counter)
    print('Signature (hex): ' + signature.hex())

    print('Is signature correct?', blocksec2go.verify_signature(public_key, hash, signature))

  except crypto_except.InvalidSignature:
    print('Verification failed!')
  except Exception as details: 
    print('ERROR: ' + str(details))
    raise SystemExit