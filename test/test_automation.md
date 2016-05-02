# Test Automation
Most of the test cases which has no dependency on environment have been automated by python unittest module

The [test_const.py](test_const.py) contains all the necessary constant required for the test verification.

The [test_conf](test_conf)	folder contains configuration files for test.


## Unit Test ##
The unit test focus on the major functions in the fibservice. The test scripts mainly verify the output of each functions.

[test_u1_fibs.py](unit_test/test_u1_fibs.py): Fibonacci number list generation function test

[test_u2_output.py](unit_test/test_u2_output.py): different output format test

[test_u3_config.py](unit_test/test_u3_config.py): configuration related test

Execute python pyunit.py to run the test cases automatically.

```
python pyunit.py
test_negative_input (test_u1_fibs.FibTestCase) ... ok
test_normal_number_input (test_u1_fibs.FibTestCase) ... ok
test_negative_input (test_u2_output.OutputTestCase) ... ok
test_normal_output (test_u2_output.OutputTestCase) ... ok
test_load_invalid_cfg (test_u3_config.ConfigTestCase) ... ok
test_load_valid_cfg (test_u3_config.ConfigTestCase) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.031s

OK
```

## Functional Test ##

The functional test focus on the web service use cases. It leverages the Flask test_client to send request to the server.

[test_f2_rest.py](func_test/test_f2_rest.py): rest request test

Execute python pyunit.py to run the test cases automatically.

```
$ python pyunit.py
test_rest_request (test_f2_rest.FibServiceTestCase) ... ok
test_rest_request_xml (test_f2_rest.FibServiceTestCase) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.395s

OK
```
