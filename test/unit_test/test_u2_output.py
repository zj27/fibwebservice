import unittest
import json
from xml.dom import minidom
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
      
        xml_str = output_formatting(self.fib1, 'xml')
        dom = minidom.parseString(xml_str)
        self.assertEqual('0 1 1 2 3', dom.getElementsByTagName('Fibonacci')[0].childNodes[0].data)   
 
        xml_str = output_formatting(self.fib2, 'xml')
        dom = minidom.parseString(xml_str)
        self.assertEqual('0', dom.getElementsByTagName('Fibonacci')[0].childNodes[0].data)   

    def test_negative_input(self):
        """
        U2-3 to U2-4
        """
        # For invalid output type, use json as default
        self.assertEqual(json.dumps(self.fib1), output_formatting(self.fib1, 'html'))

        self.assertEqual(json.dumps("hello"), output_formatting("hello", 'json'))

        xml_str = output_formatting("hello", 'xml')
        dom = minidom.parseString(xml_str)
        self.assertEqual(0, len(dom.getElementsByTagName('Fibonacci')[0].childNodes))   

        xml_str = output_formatting(1, 'xml')
        dom = minidom.parseString(xml_str)
        self.assertEqual(0, len(dom.getElementsByTagName('Fibonacci')[0].childNodes))   
