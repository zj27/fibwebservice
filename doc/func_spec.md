# Functional Specification for fibwebserivce
## Background
The project is target to implement a web service which support a REST GET call. The major function of this web service is to accept a number and return the Fibonacci numbers with the length of the given number. This project is going to be put into production and maintain for at least 5 years.
## User Cases
* The web service receives a REST GET request with a postive integer number n. The web service responds with the first n Fibonacci numbers(starting from 0)
*  The web service receives a REST GET request with a negative number, floating number, or without number. The web service responds with an appropirate error
*  The web service doesn't respond for other kinds of request

## Implementation Specification
Programming Language: Python (2.x)
### Web Service Framework
* To build a web service, python has build-in library like BaseHTTPServer. However, directly build web service based on those libraries is not effcient and robust. Therefore, a web service framework should be leveraged.
* There are lots of web service framework for python. Here are two of the most popular:
	* Django
	* Flask
  
  Flask is chosen for this project, because comparing to Django, Flask is a mircro framework which is more flexiable and suitable for such small web service product. 

### REST GET Request Handling
* The GET request url should follow the pattern as "\<host:80\>/fib/\<num\>"
	* The number should be a postive integer between 0 and 10000.
	* The upper of the scope is set as 10000, because if the number is too big, the calculation and data transmission will become very slow. And the program have the risk of crash because of memory issue.
* If the request url is invalid, the service will respond 400 or 404 with proper error message.
	* If the url direct to a different location, 404 error will be returned
	* If the url is followed by a negative number, floating number or string, 404 error will be returned.
	* If the url is followed by integer out of the supported range, 400 error will be returned with error message. 
* For the response of Fibonacci numbers, the program provides two kinds of format: json and xml.
* Http messages will be recorded into log file.

### Caching
* The service provides a simple cache which is only enabled when running by buildin server.
	* The cache will store the longest fibonacci number list which has been requested so far.
	* If the new incoming request needs a shorter list, the service could directly return part of the list from the cache without duplicated calculation.
	* Considering this service only returns fibonacci numbers, the cache will be not expired. 
* For production, the simple cache is not suffcient, so it will be disabled when deployed in a http server. Please refer to the server for caching.

### Fibonacci Number Generation
* To better leverage the advantage of python, the fibonacci number will directly be generated on a list.
* If the specified number is 0, it generates a empty list. If the number is 1, it returns [0]. If the number is bigger than 1, then it will calculate and extend the list based on [0, 1]
* If a previous existing list is get from the cache, the generation function will do the calculation based on the existing list to avoid unnecessary overhead. 

### User Customization
* As this project is targeted to put into production, the program provides configuration files for users to configure their host, port and preferred output format.
* Currently this program supports json and xml output.

```
[Server]
host=localhost
port=8000
[Output]
# support json and xml
format=json
```
### Deployment
* This project will provide a installation script to distribute the program and configuration files.
* A bz2 package which includes all the necessary files will be provided to simplify the deployment.
* A script will be provided to build the package.
* The deployment will install the binary(python file) and configuration file. User could simply run and test it. For real production, a modern web server like Apache2 is suggested.

## High Level Test Requirement
[HLTR](HLTR.md)

## Future Improvement
Because of limited schedule and resource, some potential improvements not implemented yet are recorded as follow: 
### Deployment by Docker
* The current deployment procedure is still a little complex because it has dependency on python, flask and external http server. Container may be leveraged for a quick and simple deployment. All the dependencies could be installed in the container by being specified in the dockerfile. 
### Better Caching
* Add support for external cache server like memcached.
* The normal "key-value" cache is not best for the fabonacci list. For example, if a list of 10 fibonacci numbers need to be updated as 20, it's actually not necessary to store the whole list of 20, but only need the last 10 numbers. One idea is to make the cache support "extend" the existing cache data. Another idea is the split the fibonacci number in different "key", for the same example, store the list of last 10 number into another key. But it will increase the complexity of the code to split and reconstruct the fibonacci list. 
### Compression on Response Data
* The returned fabonaaci numbers data may be big in size, so the network transmission will become the bottleneck. So the response could be compressed by encoding. And the client will decode it to get the right data.
