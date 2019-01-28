import array
import logging
from smartcard.pcsc.PCSCReader import PCSCReader
from blockchain2go.comm.base import Apdu, ApduResponse

logger = logging.getLogger(__name__)

class PySCardReader:
  def __init__(self, connection):
    self.connection = connection
    self.connection.connect()
  
  def transceive(self, header, data = b'', le = -1):
    apdu = Apdu(header, data, le)
    logger.info(apdu)
    resp = self._transceive(apdu.toBytes())
    logger.info(resp)
    return resp

  def _transceive(self, apdu):
    resp, sw1, sw2 = self.connection.transmit(array.array('b', apdu).tolist())
    return ApduResponse(array.array('B', resp).tobytes(), (sw1 << 8) + sw2)

def open_pyscard(name):
  return PySCardReader(PCSCReader(name).createConnection())