from pprint import pprint
from .exceptions import DebugException

def dd(*args):
    raise DebugException(*args)