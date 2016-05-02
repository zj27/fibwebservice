# Deployment in Apache
Here is a simple and tutorial to deploy fibwebservice in the Apache. The fibwebservice package also includes some necessary configuration file as example.

**Step 1:** Download the package and install the service as mentioned in the [quick start](../README.md).

**Step 2:** In the downloaded package, there is a fold "deploy_apache" which contains two files:

```
ls deploy_apache/
001-fibservice.conf fibservice.wsgi
``` 
Copy the wsgi file into the Apache document root folder "/var/www/"with a new created folder "fibservice"

```
$ mkdir /var/www/fibservice/
$ cp fibservice.wsgi /var/www/fibservice
```
Customize the wsgi file if necessary. The wsgi will also import the configuration from the cfg file, but will ignore the server related info.

```
import sys
sys.path.insert(0, "/usr/local/bin/")
from fibservice import app as application
from fibservice import import_configuration_wsgi
import_configuration_wsgi()
```

**Step 3:** Create Apache configuration file. The 001-fibservice.conf could be an example:

```
<VirtualHost *:80>
    ServerName localhost
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    WSGIDaemonProcess fibservice user=julius group=julius threads=5
    WSGIScriptAlias / /var/www/fibservice/fibservice.wsgi
    <Directory /var/www/fibservice>
        WSGIProcessGroup fibservice
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```

**Step 4:** Restart the Apache. The web service should be functional.
 



