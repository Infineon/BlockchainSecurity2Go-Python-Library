import blocksec2go

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

if('__main__' == __name__):
  reader = get_reader()
  activate_card(reader)

  try:
    if('Yes' == input('Do you want to create a new Keypair? ("Yes" or "No")\n')):
      key_id = blocksec2go.generate_keypair(reader)
      print('Keypair generated on slot ' + str(key_id))
  except Exception as details:
    print('ERROR: ' + str(details))
    raise SystemExit
  
  try:
    key_id = int(input('Get information on which key? (Number between 0-255 only)\n'))
    global_counter, counter, key = blocksec2go.get_key_info(reader, key_id)
  except Exception as details:
    print('ERROR: ' + str(details))
    raise SystemExit
  print('Remaining signatures with card: ' + str(global_counter))
  print('Remaining signatures with key' + str(key_id) + ': ' + str(counter))
  print('Public key (hex, encoded according to SEC1): ' + key.hex())