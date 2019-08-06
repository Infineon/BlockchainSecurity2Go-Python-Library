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
  mode = input('What would you like to do? ("Set pin", "Change pin", "Unlock pin" or "Verify pin")\n')
  try:
    if('Set pin' == mode):
      pin = input('Please enter a new PIN: ')
      puk = blocksec2go.set_pin(reader, pin)
      print('PUK to unlock card (hex): ' + puk.hex())
    elif('Change pin' == mode):
      old_pin = input('Please enter PIN: ')
      new_pin = input('Please enter a new PIN: ')
      puk = blocksec2go.change_pin(reader, old_pin, new_pin)
      print('New PUK to unlock card (hex): ' + puk.hex())
    elif('Unlock pin' == mode):
      puk = input('Please enter PUK: ')
      status = blocksec2go.unlock_pin(reader, bytes.fromhex(puk))
      if((True == status) and (isinstance(status, bool))):
        print('OK - Unlocked!')
      elif(0 != status):
        print('ERROR - ' + str(status) + ' tries left')
      else:
        print('ERROR - Card locked!')
    elif('Verify pin' == mode):
      pin = input('Please enter PIN: ')
      status = blocksec2go.verify_pin(reader, pin)
      if((True == status) and (isinstance(status, bool))):
        print('OK - Verified!')
      elif(0 != status):
        print('ERROR - ' + str(status) + ' tries left')
      else:
        print('ERROR - PIN locked! Please use "Unlock pin" command and PUK to reset PIN.')
    else:
      raise Exception('Please select one of the 4 commands!')
  except Exception as details:
    print('ERROR: ' + str(details))
    raise SystemExit