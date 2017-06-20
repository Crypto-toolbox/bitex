# Import Built-Ins
import logging
import unittest

# Import Third-Party

# Import Homebrew
from bitex.interface import Interface
from bitex.exceptions import UnsupportedPairError, EmptySupportedPairListWarning

# Init Logging Facilities
log = logging.getLogger(__name__)


class InterfaceTests(unittest.TestCase):
    def test_init_raises_NotImplementedError_for_basic_interface(self):
        iface = Interface(name='TestInterface', rest_api=None)
        self.assertIs(iface.supported_pairs, None)

        # Assert that a warning is issued if the supported_pairs attr is
        # Empty or None. Ignore the Attribute Error.
        with self.assertRaises(AttributeError):
            with self.assertWarns(EmptySupportedPairListWarning):
                iface.request('GET', 'LTCUSD', None)

        # Assert that the supported_pairs attribute cannot be set
        with self.assertRaises(AttributeError):
            iface.supported_pairs = ['Hello']

        # Assert that is_supported() method evaluates as expected. To test this,
        # circumvent overwrite protection of supported_pairs attribute.
        iface._supported_pairs = ['BTCUSD', 'LTCBTC']

        self.assertTrue(iface.is_supported('BTCUSD'))
        self.assertTrue(iface.is_supported('LTCBTC'))
        self.assertFalse(iface.is_supported('LTCUSD'))

        # Assert that, by default, _get_supported_pairs() raises a
        # NotImplementedError
        with self.assertRaises(NotImplementedError):
            iface._get_supported_pairs()

if __name__ == '__main__':
    unittest.main()
