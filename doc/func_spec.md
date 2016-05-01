# Functional Specification for fibwebserivce
## Background
The project is target to implement a web service which support a REST GET call. The major function of this web service is to accept a number and return the Fibonacci numbers with the length of the given number. This project is going to be put into production and maintain for at least 5 years.
## User Cases
* The web service receives a REST GET request with a postive integer number n. The web service response with the first n Fibonacci numbers(starting from 0)
*  The web service receives a REST GET request with a negative number, floating number, or without number. The web service response with an appropirate error
*  The web service doesn't response for other kinds of request

## Implementation Specification
Programming Language: Python (2.x)
### Web Service Framework
* To build a web service, python has build-in library like BaseHTTPServer. However, directly build web service based on those libraries is not effcient and robust. Therefore, a web service framework should be leveraged.
* There are lots of web service framework for python. Here are two of the most popular:
	* Django
	* Flask
  
  Flask is chosen for this project, because comparing to Django, Flask is a mircro framework which is more flexiable and suitable for such small web service product. 

### REST GET Request Handling
* For the response of Fibonacci numbers, the program provides two kinds of format: json and xml.
* If the request provides invalid number or no number, the program will response 400 or 404 with proper error message.
* The length of fibonacci number list should be between 0 and 10000. If the length is too long, the value may overflow. 
* Http messages will be recorded into log file.

### Fibonacci Number Generation
* To better leverage the advantage of python, the fibonacci number will directly generated on a list.
* If the specified number is 0, it generates a empty list. If the number is 1, it returns [0]. If the number is bigger than 1, then it will calculate and extend the list based on [0, 1]

### User Customization
* As this project is targeted to put into production, the program provides configuration files for users to configure their host, port and preferred output format.
* Currently this program support json and xml output.

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

