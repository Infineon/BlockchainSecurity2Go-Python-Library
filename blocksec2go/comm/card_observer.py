from smartcard.CardMonitoring import CardMonitor, CardObserver

class card_observer(CardObserver):
  """ Monitors smartcard

  Monitors insertion or removal of smartcard. Calls functions in 
  case of insertion/removal.
  """
  def connect(self):
    pass

  def disconnect(self):
    pass

  def update(self, observable, actions):
    (addedcards, removedcards) = actions
    for card in addedcards:
      self.connect()
    for card in removedcards:
      self.disconnect()

class observer:
  """ Wrapper for card observer
  
  Abstracts communication into simple functions so that the user
  doesn't have to communicate with ``CardMonitoring`` library
  """
  def start():
    cardmonitor = CardMonitor()
    cardobserver = card_observer()
    cardmonitor.addObserver(cardobserver)
    return (cardmonitor, cardobserver)

  def stop(cardmonitor, cardobserver):
    cardmonitor.deleteObserver(cardobserver)