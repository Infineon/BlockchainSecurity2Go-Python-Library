import array
import logging
from smartcard.pcsc.PCSCReader import PCSCReader
from blockchain2go.comm.base import Apdu, ApduResponse

logger = logging.getLogger(__name__)

class PySCardReader:
    """ Wrapper to use PyScard with blockchain2go
    
    Abstracts communication into a simple function
    """
    def __init__(self, connection):
        self.connection = connection
        self.connection.connect()
    
    def transceive(self, header, data = b'', le = -1):
        apdu = Apdu(header, data, le)
        logger.debug(apdu)
        resp = self._transceive(bytes(apdu))
        logger.debug(resp)
        return resp

    def _transceive(self, data):
        resp, sw1, sw2 = self.connection.transmit(array.array('b', data).tolist())
        return ApduResponse(array.array('B', resp).tobytes(), (sw1 << 8) + sw2)

def open_pyscard(name):
    """ Open PC/SC reader using PyScard

    Args:
        name (:obj:`str`): name of the reader as registered in the system
    
    Returns:
        :obj:`PyScardReader`: PyScard wrapper object
    
    Raises:
        Various PyScard exceptions
    """
    return PySCardReader(PCSCReader(name).createConnection())