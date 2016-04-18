import unittest
import json
from fibservice import output_formatting

class OutputTestCase(unittest.TestCase):
    """
    Unit test cases for output
    """
    def setUp(self):
        """
        Pass
        """
        self.fib1 = [0, 1, 1, 2, 3]
        self.fib2 = [0]

    def tearDown(self):
        """
        Pass
        """
        pass

    def test_normal_output(self):
        """
        U2-1 to U2-2
        """
        self.assertEqual(json.dumps(self.fib1), output_formatting(self.fib1, 'json'))
        self.assertEqual(json.dumps(self.fib2), output_formatting(self.fib2, 'json'))
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><fib>0 1 1 2 3</fib>', 
                         output_formatting(self.fib1, 'xml'))
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><fib>0</fib>', 
                         output_formatting(self.fib2, 'xml'))

    def test_negative_input(self):
        """
        U2-3 to U2-4
        """
        # For invalid output type, use json as default
        self.assertEqual(json.dumps(self.fib1), output_formatting(self.fib1, 'html'))

        self.assertEqual(json.dumps("hello"), output_formatting("hello", 'json'))

        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><fib></fib>', output_formatting("hello", 'xml'))
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><fib></fib>', output_formatting(1, 'xml'))
