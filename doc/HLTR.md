# High Level Test Requirement
## Web Service
### Normal Functionality
* The web service is able to start
* The web service response GET request with correct Fibonacci numbers 

### Reliability(Negative Case)
* The web service response with error when the GET request provides invalid number
* The web service response with error when the GET request provides no number
* The web service response nothing for other kinds of request

## Configuration
### Normal Functionality
* The web service is able to read the configuration file and works with the customized configuration. 

### Reliability(Negative Case)
* If the configuration file is not available, the web service runs with default configuration.
* If the entries in the configuration is not valid, the web service runs with default configuration.

## Deployment
### Normal Functionality
* The deployment script copies the files into the correct location.
