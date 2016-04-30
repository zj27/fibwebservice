import unittest

import fibservice

class FibServiceTestCase(unittest.TestCase):
    """
    Test cases for fibservice
    """
    def setUp(self):
        """
        Pass
        """
        self.app = fibservice.app.test_client()

    def tearDown(self):
        """
        Pass
        """
        pass

    def test_rest_request(self):
        """
        """ 
        fibservice.default_configuration()

        rv = self.app.get("/")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib/1")
        self.assertEqual(200, rv.status_code)
        self.assertEqual("[0]", rv.data)
