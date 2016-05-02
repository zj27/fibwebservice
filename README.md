# fibwebservice
A simple web service which returns Fibonacci numbers with specified length between 0 and 10000.
# Quick Start
This quick start shows how to quickly deploy and run the fibwebservice.
## System Requirement
* Linux platform is preferred
* Python 2.x (2.6 or 2.7 is recommended)
* [Flask](http://flask.pocoo.org) (the latest 0.10.1 is recommended)  

## Installation
1. Download the package **fibwebservice.tar.bz2**, or download the entire source and execute the **build.sh** to generate the package. Compare the md5 with **fibwebservice.tar.bz2.md5**
2. Extract the **fibwebservice.tar.bz2** to an empty folder
<pre>
<code>tar -xvf fibwebservice.tar.bz2 -C fibwebservice/</code>
</pre>
3. Execute the **install.sh** (with root privilege)to install the web service.

## Running the web service
Here is a simple guide on how to directly run this web service. For production, please integrate it with a http server. Next section shows an example of deployment in Apache. 

1. Customize the configuration at **/etc/fibserver.cfg**

   ```
   [Server]
   host=localhost
   port=8000
   [Output]
   # support json and xml
   format=json
   ```
2. Execute **fibservice.py**

	```
	# fibservice.py
	Starting server, use <Ctrl-C> to stop
	```
	
3. Use client program, browser or curl to send GET request with a positive number at the end of url.

	```
	curl http://10.32.118.201:8000/fib/10
	[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
	```

## Deploy in a http server
The buildin server is sufficient for development, but not good enough for real production.

Here is a simple [tutorial for Apache](doc/deploy_apache.md).

For other deployment options, please refer to the [offical Flask doc](http://flask.pocoo.org/docs/0.10/deploying/)

# Resources

+ [**doc**](doc/) - contains all project documents
   + [Design doc](doc/func_spec.md)
+ [**src**](src/) - contains the source codes
+ [**package**](package/) - contains the bz2 for deployment
+ [**test**](test/) - contains test case and test scripts
   + [Test cases](test/test_cases_summary.md)
   + [Test Automation](test/test_automation.md)
