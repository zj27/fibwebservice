# fibwebservice
A simple web service which returns Fibonacci numbers with length between 0 and 10000.
# Quick Start
## Installation
1. Download the package **fibwebservice.tar.bz2**, or download the entire source and execute the **build.sh** to generate the package. Compare the md5 with **fibwebservice.tar.bz2.md5**
2. Extract the **fibwebservice.tar.bz2** to an empty folder
<pre>
<code>tar -xvf fibwebservice.tar.bz2 -C fibwebservice/</code>
</pre>
3. Execute the **install.sh** to install the web service.

## Running the web service
1. Customize the configuration at **/etc/fibserver.cfg**

   ```
   [Server]
   host=""
   port=8000
   [Output]
   # support json and xml
   format=json
   ```
2. Execute **fibservice.py**

    ```
    # fibservice.py
    Starting server, useg <Ctrl-C> to stop
    ```
3. Use client program, browser or curl to send GET request with a positive number at the end of url.

    ```
    curl http://10.32.118.201:8000/10
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    ```

## Resources

+ [**doc**](doc/) - contains all project documents
   + [Design doc](doc/func_spec.md)
+ [**src**](src/) - contains the source codes
+ [**package**](package/) - contains the bz2 for deployment
+ [**test**](test/) - contains test case and test scripts
   + [Test cases](test/test_cases_summary.md)
