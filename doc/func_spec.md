# Functional Specification for fibwebserivce
## Background
The project is target to implement a web service which support a REST GET call. The major function of this web service is to accept a number and return the Fibonacci numbers with the length of the given number. This project is going to be put into production and maintain for at least 5 years.
## User Cases
* The web service receives a REST GET request with a postive integer number n. The web service response with the first n Fibonacci numbers(starting from 0)
*  The web service receives a REST GET request with a negative number, floating number, or without number. The web service response with an appropirate error
*  The web service doesn't response for other kinds of request

## Implementation Specification
Programming Language: Python
### REST GET Request Handling
* The program will leverage BaseHTTPServer.HTTPServer to implement the web service. Comparing to the third-party framework, the build-in python module will make it easier for deployment and maintenance.
* To serve large amount of request, the program will use ThreadingMixIn, thus each request will be handled by a different thread
* For the response of Fibonacci numbers, json may be the best format. However, the program will leave interface in case it need more kinds for format in the future.
* If the request provides invalid number or no number, the program will response 400 with proper error message.

### Fibonacci Number Generation
* To better leverages the advantage of python, the fibonacci number will directly generated on a list.
* If the specified number is 0, it generates a empty list. If the number is 1, it returns [0]. If the number is bigger than 1, then it will calculate and extend the list based on [0, 1]

### User Customization
* As this project is targeted to put into production, the program provides configuration files for users to configure their host, port and preferred output format.
* Currently this program only support json so far
```
[Server]
host=localhost
port=8000
[Output]
# support json only so far
format=json
```
### Deployment
* This project will provide a installation script to distribute the program and configuration files.
* A package which includes all the necessary files will be provided to simplify the deloyment.

## High Level Test Requirement
[HLTR](HLTR.md)

## Future Improvement
Because of limited schedule and resource, this project only provides major functions at this stage. As this project will be put into production and maintain for 5 years, following improvement is planned:

### Daemon
* For better deployment and operation, the program should support run as a daemon. The service should be able to directly start, stop and restart. All the current output of the program should be redirect into log files.

### Server-side Cache
* For better performance at server side, the program should implement a server-side cache to store recent request result(eg. last 100 query) which could avoid some duplicated calculation.

### User Authentication
* In the production, the service may only serve for certain users. It should provide user authentication to block unauthorized request.

### Multiple OS support
* Currently the service only support Linux platform because of the implantation of configuration files. To expand our market, the program should support more OS like windows.
