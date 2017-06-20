# Import Built-Ins
import logging
import unittest

# Import Third-Party

# Import Homebrew
from bitex.interface import Interface
from bitex.exceptions import UnsupportedPairError

# Init Logging Facilities
log = logging.getLogger(__name__)


class InterfaceTests(unittest.TestCase):
    def test_init_raises_NotImplementedError_for_basic_interface(self):
        with self.assertRaises(NotImplementedError):
            Interface(name='TestInterface', rest_api=None)


if __name__ == '__main__':
    unittest.main()
