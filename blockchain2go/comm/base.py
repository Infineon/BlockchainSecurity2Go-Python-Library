ERRORS = {
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
    def __init__(self, message, response=None):
        self.message = message
        self.response = response
        super(CardError, self).__init__(message)
    
    def __str__(self):
        if self.response is not None:
            return self.message + ' ' + str(self.response)
        else:
            return self.message

    def __repr__(self):
        return 'CardError(' + self.message + ', ' + str(self.response) + ')'


class ApduResponse:
    def __init__(self, resp, sw):
        self.resp = resp
        self.sw = sw

    def __bool__(self):
        return self.sw == 0x9000

    def check(self):
        if self.sw != 0x9000:
                raise CardError('card indicated failure', self)
        return self
    
    def __str__(self):
        text = ""
        if (self.sw & 0xFFF0) == 0x63C0:
            text = 'Authentication failed - {} tries remaining'.format(self.sw & 0xF)
        elif (self.sw & 0xFF00) == 0x6400:
            text = 'Operation failed - fatal error {}'.format(self.sw & 0xFF)
        elif self.sw in ERRORS:
            text = ERRORS[self.sw]
        
        return 'response ' + self.resp.hex() + ' (' + str(len(self.resp)) + ') ' + hex(self.sw) + ' ' + text


class Apdu:
    def __init__(self, header, data = None, le = None):
        if len(header) != 4:
            raise ValueError('invalid header length: ' + str(header) + ' (' + str(len(header)) + ')')
        if len(data) > 255 or le > 256:
            raise RuntimeError('extended length APDU support not yet implemented')

        self.header = header
        self.data = data
        self.le = le

    def __bytes__(self):
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