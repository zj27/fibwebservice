# Test Cases Summary
Here is the summary of all the test cases for this project. <br>
Some of the cases have been implented with automation scripts included in the corresponding folders.
# Unit Test
## U1 Fibonacci Numbers Generation Function
+ U1-1 call the function with normal random positive integer number. 
+ U1-2 call the function with negative number.
+ U1-3 call the function with floating number.
+ U1-4 call the function with string
+ U1-5 call the function with very big number.

## U2 Output Formatting
+ U2-1 call the function with json output
+ U2-2 call the function with xml output
+ U2-3 call the function with unknown output
+ U2-4 call the function with invalid fib list

## U3 Import Configuration
+ U3-1 call the function to load a valid config file
+ U3-2 call the function to load a empy file
+ U3-3 call the function to load a non-config file
+ U3-4 call the function with invalid config entries

# Functional Test
## F1 Installation/Deployment
+ F1-1 Execute the installation script
	+ Check if the binary(py) and cfg files are correctly deployed.

## F2 Web Service
+ F2-1 Start web service
	+ Send GET request with random valid number
	+ Send GET request with negative/floating/big number
	+ Send GET request without number
	+ Send other kinds of request

+ F2-2 Start multiple web services on same port

## F3 Customize configuration
+ F3-1 Change the host and port with valid value, and start the web service
+ F3-2 Change the host and port with invalid value, and start the web service
+ F3-3 Change the output format to json or xml, cover F2-1 for both cases
+ F3-4 Change the output format to unknown type

# Performance Test
Evaluate the performance of the web services:<br>
1. Leverage load test framework or scripts to create multiple processes/threads to send GET request to the web services with random number.<br>
2. Calculate the latency of each request.<br>
3. Summarize the max, min and average latency.<br>
