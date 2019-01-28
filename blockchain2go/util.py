import argparse

def bytes_from_hex(expected_len=None):
  def _bytes_from_hex(string):
    b = None
    try:
      b = bytes.fromhex(string)
    except Exception as e:
      raise argparse.ArgumentTypeError('could not parse "' + string + '" as hex-encoded hash', e)
    
    if expected_len is not None and len(b) != expected_len:
      raise argparse.ArgumentTypeError('invalid length, must be {} bytes long'.format(expected_len))
    
    return b

  return _bytes_from_hex