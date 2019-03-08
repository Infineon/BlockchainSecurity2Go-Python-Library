import array
import logging
import smartcard.System
from smartcard.pcsc.PCSCReader import PCSCReader
from blocksec2go.comm.base import Apdu, ApduResponse

logger = logging.getLogger(__name__)

class PySCardReader:
    """ Wrapper to use PyScard with blocksec2go
    
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

def open_pyscard(name=None):
    """ Open PC/SC reader using PyScard
        If no reader name is given, try to open all available readers, 
        the first one that succeeds is chosen.

    Args:
        name (:obj:`str`): name of the reader as registered in the system
    
    Returns:
        :obj:`PyScardReader`: PyScard wrapper object
    
    Raises:
        RuntimeError exception if no reader can be opened
        Various PyScard exceptions
    """
    if name is not None:
        return PySCardReader(PCSCReader(name).createConnection())
    else:
        readers = smartcard.System.readers()
        for reader in readers:
            try:
                pyscardreader = PySCardReader(PCSCReader(reader).createConnection())
            except:
                pass
            else:
                logger.debug("Open reader: %s", reader)
                return pyscardreader

        raise RuntimeError('No reader with card found. Available readers: ', readers)
