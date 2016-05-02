import sys
sys.path.insert(0, "/usr/local/bin/")
from fibservice import app as application
from fibservice import import_configuration_wsgi
import_configuration_wsgi()
