#!/usr/bin/python

"""
A simple web service returns first n Fibonacci numbers
"""

import ConfigParser
import json
import logging
import os
import sys
from xml.dom import minidom

from flask import Flask
from flask import abort
from werkzeug.contrib.cache import SimpleCache 
app = Flask(__name__)


LOG_FILE = "/var/log/fibwebservice.log"
CONFIG_FILE = "/etc/fibservice.cfg"
FAILURE = 1
SUCCESS = 0
VALID_PORT_RANGE = range(1024, 65536) 
VALID_OUTPUT_FORMAT = ['json', 'xml']
FIB_MAX = 10000
VALID_FIB_RANGE = range(1, FIB_MAX + 1)

def exit_with_msg(msg):
    """
    Print the specified message, and exit with failure
    """
    print msg
    sys.exit(FAILURE)

def default_configuration():
    """
    Generate default configuration
    """
    app.config["host"] = "localhost"
    app.config["port"] = 8000
    app.config["output_format"] = 'json'
    app.config["local_cache"] = None

def is_port_valid(port):
    """
    Check if the port is valid
    """
    if port in VALID_PORT_RANGE:
        return True
    else:
        return False

def is_output_format_valid(output_format):
    """
    Check if the format is valid
    """
    if output_format in VALID_OUTPUT_FORMAT:
        return True
    else:
        return False

def import_configuration_wsgi(config_file = CONFIG_FILE):
    """
    Import the configuration by wsgi. Ignore server related entries
    """
    try:
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(config_file)
        app.config["output_format"] = config_parser.get("Output", "format")
    except ConfigParser.Error:
        default_configuration()

    if not is_output_format_valid(app.config["output_format"]):
        default_configuration()

    # Do not use local cache when integrated with a wsgi server
    app.config["local_cache"] = None

def import_configuration(config_file):
    """
    Import basic configuration for conf file
    """

    try:
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(config_file)
        app.config["host"] = config_parser.get("Server", "host")
        app.config["port"] = config_parser.getint("Server", "port")
        app.config["output_format"] = config_parser.get("Output", "format")
    except ConfigParser.Error:
        print "Error during loading configuration file. Use default configuration"
        default_configuration()

    if not is_port_valid(app.config["port"]):
        return FAILURE, "Invalid port %d" % app.config["port"]
    if not is_output_format_valid(app.config["output_format"]):
        return FAILURE, "Invalid output format %s" % app.config["output_format"]

    app.config["local_cache"] = SimpleCache()

    return SUCCESS, None

def generate_fib_xml(fib_list):
    """
    Generate a xml with fib list
    """
    try:
        for i in range(0, len(fib_list)):
            fib_list[i] = str(fib_list[i])
        fib_str = str(" ").join(fib_list)
    except TypeError, msg:
        logging.error(msg)
        fib_str = ""
    doc = minidom.Document()
    fib = doc.createElement("Fibonacci")
    doc.appendChild(fib)
    fib.appendChild(doc.createTextNode(fib_str))
    return doc.toprettyxml()

def output_formatting(fib_list, output_format):
    """
    Convert the fib list into specified format
    """
    if output_format == "json":
        return json.dumps(fib_list)
    elif output_format == "xml":
        return generate_fib_xml(fib_list)
    else:
        # return json format as default
        return json.dumps(fib_list)
    return

def fibs(num, base=None):
    """
    Return the fib list with specified number
    The base parameter provides a known fib list, 
    so the calculation could continue on that
    """
    
    if num not in VALID_FIB_RANGE:
        return []

    if num == 1:
        return [0]
    else:
        result = None
        start, end = 0, 0
        if base == None or type(base) != list or len(base) < 2:
            # calculating from 0
            result = [None] * num
            result[0] = 0
            result[1] = 1
            start = 2
            end = num
        else:
            # calculating from base
            result = base 
            start = len(base)
            end = num
            result.extend([None] * (end - start))

        try:
            for i in range(start, end):
                result[i] = result[i-2] + result[i-1]
        except (ValueError, IndexError, TypeError), msg:
            logging.error("Error during generating the fib list: %s" % msg)
            return []
        return result

@app.route("/fib/<int:num>")
def get_fib_nums(num):
    """
    Handle Get Request to get fibonacci numbers
    """
    # range check
    if num not in VALID_FIB_RANGE:
        abort(400)

    fib_list = None

    # try to search existing result from cache
    if app.config["local_cache"] != None:
        fib_list = app.config["local_cache"].get("fibs")
    if fib_list != None and len(fib_list) >= num:
        logging.debug("Hit Cache!")
        fib_list = fib_list[:num]
        if len(fib_list) == 0:
            abort(400)
    else:
        # calcualte the fibs based on the existing cache result
        fib_list = fibs(num, fib_list)
        if len(fib_list) == 0:
            abort(400)
        # update the cache to store the latest result
        if app.config["local_cache"] != None:
            app.config["local_cache"].set("fibs", fib_list)
            logging.info("Updating cache with fib list of %d length" % num)

    return output_formatting(fib_list, app.config['output_format'])

@app.errorhandler(400)
def bad_request(error):
    """
    Handle bad request
    """
    return "The fibonaaci numbers length is limited between 0 and %s" % FIB_MAX, 400

def set_logging(log_file_path, env_loglevel = None):
    """
    Set the logging file and format of an application which uses python logging module.
    """
    # Create the directory if it does not exist
    directory = os.path.dirname(log_file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError, msg:
            exit_with_msg("Failed to create the log directory of %s, %s." % (directory, msg))

    # Get log level, default value is Info
    # Dev can change this by dynamically export LOG_LEVEL env
    DEFAULT_LOGLEVEL = logging.INFO

    if env_loglevel is None:
        env_loglevel = os.getenv("PYLIB_LOGLEVEL")
    if env_loglevel is None:
        # If not defined, set as default value
        log_level = DEFAULT_LOGLEVEL
    else:
        # Else, get customized one
        env_loglevel = env_loglevel.upper()

        if env_loglevel == "DEBUG":
            log_level = logging.DEBUG
        elif env_loglevel == "INFO":
            log_level = logging.INFO
        elif env_loglevel == "WARNING":
            log_level = logging.WARNING
        elif env_loglevel == "ERROR":
            log_level = logging.ERROR
        elif env_loglevel == "CRITICAL":
            log_level = logging.CRITICAL
        else:
            log_level = DEFAULT_LOGLEVEL

    # Set logging file and format
    try:
        logging.basicConfig(level=log_level, filename=log_file_path, 
            format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s")
    except IOError, msg:
        exit_with_msg("Failed to set the log file, %s" % msg)

def run():
    """
    Main function to run the web service
    """

    set_logging(LOG_FILE)
    status, output = import_configuration(CONFIG_FILE)
    if status != SUCCESS:
        exit_with_msg(output)

    app.run(app.config['host'], app.config['port'], threaded = True)

if __name__ == "__main__":
    try:
        run()
    except Exception, msg:
        # leave no exceptions to the user.
        exit_with_msg(msg)

