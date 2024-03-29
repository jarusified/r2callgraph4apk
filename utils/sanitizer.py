import os


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
class Sanitizer:

    _KNOWN_TYPES = ["function", "statement", "loop", "region"]

    @staticmethod
    def sanitize(_: str):
        return os.path.basename(_) if _ is not None else 'Unknown'

    @staticmethod
    def from_r2(_: ):

        _type = _['type']
        assert _type in Sanitizer._KNOWN_TYPES

        if _type in ['function', 'region']:
            return Sanitizer.sanitize(_.get('name', 'Unknown'))

        elif _type == 'statement':
            _file, _line = _['file'], str(_['line'])
            return Sanitizer.sanitize(_file) + ':' + _line

        elif _type == 'loop':
            _file, _line = _['file'], str(_['line'])
            return 'Loop@' + Sanitizer.sanitize(_file) + ':' + _line

# ------------------------------------------------------------------------------
