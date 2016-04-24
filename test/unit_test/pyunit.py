import unittest
import test_u1_fibs
import test_u2_output
import test_u3_config

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_u1_fibs))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_u2_output))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_u3_config))

    # Run the whole test suite
    unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)  
