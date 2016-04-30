import unittest
import test_f2_rest

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test_f2_rest))

    # Run the whole test suite
    unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)  
