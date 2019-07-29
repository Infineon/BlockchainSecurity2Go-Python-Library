import blocksec2go

if('__main__' == __name__):
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
        print('ERROR:', details)
        raise SystemExit
  try:
    pin_active, card_id, version = blocksec2go.select_app(reader)
    print('Found the specified reader and a Blockchain Security 2Go card!')
  except Exception as details:
    print('ERROR:', details)
    raise SystemExit
  print('Is PIN enabled?', pin_active)
  print('Card ID (hex):', card_id.hex())
  print('Version: ' + version)