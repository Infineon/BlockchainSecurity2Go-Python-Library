import sys
from time import sleep
import blocksec2go
from blocksec2go.comm import observer

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

def connected(self):
  print('A smartcard is connected to the reader!')
  reader = get_reader()
  activate_card(reader)

def disconnected(self):
  print('The card is disconnected from the reader!')

if('__main__' == __name__):
  print("Insert a Blockchain Security 2Go card onto the reader!")
  cardmonitor, cardobserver = observer.start()
  sleep(1)
  blocksec2go.add_callback(connect = connected, disconnect = disconnected)
  print('Press Enter at any time to exit the program!')
  sys.stdin.read(1)
  observer.stop(cardmonitor, cardobserver)