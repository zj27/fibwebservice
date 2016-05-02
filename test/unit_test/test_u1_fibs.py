import unittest

from fibservice import fibs
import test_const

class FibTestCase(unittest.TestCase):
    """
    Unit test cases for fibs function
    """
    def setUp(self):
        """
        Pass
        """
        pass

    def tearDown(self):
        """
        Pass
        """
        pass

    def test_normal_number_input(self):
        """
        U1-1
        """
        self.assertEqual([], fibs(0))
        self.assertEqual(test_const.FIB_1, fibs(1))
        self.assertEqual(test_const.FIB_2, fibs(2))
        self.assertEqual(test_const.FIB_5, fibs(5))
        self.assertEqual(test_const.FIB_100, fibs(100))

    def test_negative_input(self):
        """
        U1-2 to U1-5
        """
        self.assertEqual([], fibs(-1))
        self.assertEqual([], fibs(1.1))
        self.assertEqual([], fibs("1"))

        # Upper Boundary
        self.assertEqual([], fibs(10001))
        self.assertEqual(test_const.FIB_10000_LAST, fibs(10000)[-1])
      
    def test_fib_with_base(self):
        """
        """
        self.assertEqual(test_const.FIB_2, fibs(2, test_const.FIB_1))
        self.assertEqual(test_const.FIB_3, fibs(3, test_const.FIB_1))
        self.assertEqual(test_const.FIB_3, fibs(3, test_const.FIB_2))
        self.assertEqual(test_const.FIB_5, fibs(5, test_const.FIB_2))
        self.assertEqual(test_const.FIB_100, fibs(100, test_const.FIB_5))
        # negative input
        self.assertEqual(test_const.FIB_5, fibs(5, 5))
        self.assertEqual(test_const.FIB_5, fibs(5, "hello"))
        
