import argparse

def bytes_from_hex(expected_len=None):
    """ Convert and check hex argument to bytes

    Returns a function that will convert a given hexadecimal string
    and convert it to ``bytes``. Function will check the length if 
    requested.

    Args:
        expected_len (int): expected length of resulting byte string, ``None`` to not check
    
    Returns:
        :obj:`function`: function that converts and checks

        Args:
            string (:obj:`str`): hex string
        
        Returns:
            :obj:`bytes`: converted binary data
        
        Raises:
            argparse.ArgumentTypeException: For invalid hex encoding
            or invalid length.
    
    Example:
        
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('arg', type=bytes_from_hex(16))
    """
    def _bytes_from_hex(string):
        b = None
        try:
            b = bytes.fromhex(string)
        except Exception as e:
            raise argparse.ArgumentTypeError('could not parse "' + string + '" as hex-encoded value', e)
        
        if expected_len is not None and len(b) != expected_len:
            raise argparse.ArgumentTypeError('invalid length of {} bytes, must be {} bytes long'.format(len(b), expected_len))
        
        return b

    return _bytes_from_hex