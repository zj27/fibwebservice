import unittest

from fibservice import get_configuration, import_configuration, FAILURE

class ConfigTestCase(unittest.TestCase):
    """
    Unit test cases for loading configuration
    """
    def setUp(self):
        """
        Pass
        """
        self.default_config = {
            "host": "localhost",
            "port": 8000,
            "output_format": "json"
        }

    def tearDown(self):
        """
        Pass
        """
        pass

    def test_load_valid_cfg(self):
        """
        U3-1  
        """
        import_configuration("test_conf/test_u3_1.cfg")
        config = get_configuration()
        self.assertEqual("192.168.1.1", config["host"])
        self.assertEqual(8100, config["port"])
        self.assertEqual("xml", config["output_format"])

    def test_load_invalid_cfg(self):
        """
        U3-2 to U3-4
        """
        import_configuration("test_conf/test_u3_2.cfg")
        self.assertEqual(self.default_config, get_configuration())

        import_configuration("test_conf/test_u3_3.cfg")
        self.assertEqual(self.default_config, get_configuration())

        status, _ = import_configuration("test_conf/test_u3_4_1.cfg")
        self.assertEqual(FAILURE, status)

        status, _ = import_configuration("test_conf/test_u3_4_2.cfg")
        self.assertEqual(FAILURE, status)


