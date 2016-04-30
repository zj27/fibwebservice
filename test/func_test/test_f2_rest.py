import unittest
from xml.dom import minidom

import fibservice
import test_const


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
        Functional test for rest request
        """ 
        fibservice.default_configuration()

        rv = self.app.get("/")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib/1")
        self.assertEqual(200, rv.status_code)
        self.assertEqual(str(test_const.FIB_1), rv.data)

        rv = self.app.get("/fib/5")
        self.assertEqual(200, rv.status_code)
        self.assertEqual(str(test_const.FIB_5), rv.data)

        rv = self.app.get("/fib/100")
        self.assertEqual(200, rv.status_code)
        self.assertEqual(test_const.FIB_100[-1], int(rv.data[1:-1].split(",")[-1]))

        rv = self.app.get("/fib/10000")
        self.assertEqual(200, rv.status_code)
        self.assertEqual(test_const.FIB_10000_LAST, int(rv.data[1:-1].split(",")[-1]))

        rv = self.app.get("/fib/0")
        self.assertEqual(400, rv.status_code)

        rv = self.app.get("/fib/%d" % (fibservice.FIB_MAX + 1))
        self.assertEqual(400, rv.status_code)

        rv = self.app.get("/fib/-1")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib/1.1")
        self.assertEqual(404, rv.status_code)

        rv = self.app.get("/fib/hello")
        self.assertEqual(404, rv.status_code)

        rv = self.app.post("/fib/1")
        self.assertEqual(405, rv.status_code)

        rv = self.app.put("/fib/1")
        self.assertEqual(405, rv.status_code)

    def test_rest_request_xml(self):
        """
        Test normal rest request with xml output
        """
        fibservice.import_configuration("test_conf/test_u3_1.cfg")

        rv = self.app.get("/fib/5")
        self.assertEqual(200, rv.status_code)
        dom = minidom.parseString(rv.data)
        self.assertEqual(test_const.FIB_5_STR, dom.getElementsByTagName('Fibonacci')[0].childNodes[0].data)   

        rv = self.app.get("/fib/1")
        self.assertEqual(200, rv.status_code)
        dom = minidom.parseString(rv.data)
        self.assertEqual(test_const.FIB_1_STR, dom.getElementsByTagName('Fibonacci')[0].childNodes[0].data)   
