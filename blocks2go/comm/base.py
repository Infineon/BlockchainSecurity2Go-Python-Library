_ERRORS = {
    0x6700: 'Invalid length',
    0x6983: 'Authentication failed - Locked',
    0x6985: 'Condition of use not satisfied - no active PIN session/invalid PIN state for command',
    0x6A80: 'Invalid serialization of data',
    0x6A82: 'Security status not satisfied - counter exceeded',
    0x6A84: 'Not enough memory - key storage full',
    0x6A88: 'Referenced data not found - key with the given index is not available',
    0x6A86: 'Incorrect parameters P1/P2',
    0x6A87: 'Lc inconsistent',
    0x6D00: 'INS is not supported (App may not be selected)',
    0x6E00: 'CLA is not supported',
    0x6F00: 'Unknown error',
    0x9000: 'Success',
}

class CardError(Exception):
    """ Exception if card indicates failure

    Args:
        message (str): exception message
        explanation (str, optional): possible error explanation
            ``None`` to set according to response status word
        response (:obj:`ApduResponse`, optional): raw response
            received from card

    Attributes:
        message (str): exception message
        explanation (str): error explanation if available
        response (int): returned status word of card
    """
    def __init__(self, message, response, explanation=None):
        super(CardError, self).__init__(message)
        self.message = message
        self.explanation = explanation
        self.response = response
    
    def __str__(self):
        string = self.message
        if self.explanation is not None:
            string += str(self.explanation)
        if self.response is not None:
            if self.explanation is not None:
                string += ' ('
            string += str(self.response)
            if self.explanation is not None:
                string += ')'
        return string

    def __repr__(self):
        return 'CardError(' + self.message + ', ' + self.explanation + ', ' + repr(self.response) + ')'


class ApduResponse:
    """ Cards response to command

    Args:
        resp (bytes): data portion of response
        sw (int): status word

    Attributes:
        resp (bytes): data portion of response
        sw (int): status word
    """
    def __init__(self, resp, sw):
        self.resp = resp
        self.sw = sw

    def __bool__(self):
        return self.sw == 0x9000

    def check(self):
        if self.sw != 0x9000:
            raise CardError('Card indicated failure: ', response=self)
        return self
    
    def __str__(self):
        text = ""
        if (self.sw & 0xFFF0) == 0x63C0:
            text = 'Authentication failed - {} tries remaining'.format(self.sw & 0xF)
        elif (self.sw & 0xFF00) == 0x6400:
            text = 'Operation failed - fatal error {}'.format(self.sw & 0xFF)
        elif self.sw in _ERRORS:
            text = _ERRORS[self.sw]
        
        return hex(self.sw) + ' ' + text
    
    def __repr__(self):
        return 'ApduResponse(' + repr(self.resp) + ', ' + repr(self.sw) + ')'


class Apdu:
    """ Command to send to card

    According to ISO7816-3

    Args:
        header (bytes): CLA, INS, P1, P2 bytes
        data (bytes, optional): data field of APDU
        le (int): expected response length
            ``None`` for no response
            ``-1`` for maximum size dependent on short/extended APDU
    """
    def __init__(self, header, data = None, le = None):
        if len(header) != 4:
            raise ValueError('invalid header length: ' + str(header) + ' (' + str(len(header)) + ')')
        if len(data) > 255 or le > 256:
            raise RuntimeError('extended length APDU support not yet implemented')

        self.header = header
        self.data = data
        self.le = le

    def __bytes__(self):
        """ Encode APDU as bytes
        """
        apdu = b''
        apdu += self.header
        if len(self.data) > 0:
            apdu += bytes([len(self.data)])
            apdu += self.data
        
        if self.le < 0:
            apdu += b'\x00'
        if self.le > 0:
            apdu += bytes([self.le])
        
        return apdu
    
    def __str__(self):
        leByte = None
        if self.le < 0:
            leByte = '00'
        if self.le > 0:
            leByte = bytes([self.le]).hex()

        s = 'apdu ' + self.header.hex()
        if self.data is not None:
            s += ' ' + self.data.hex()
        if leByte is not None:
            s+=  ' ' + leByte
        return s
    
    def __repr__(self):
        return 'Apdu(' + repr(self.header) + ', ' + repr(self.data) + ', ' + repr(self.le) + ')'