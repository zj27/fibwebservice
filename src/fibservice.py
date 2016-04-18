#!/usr/bin/python

"""
A simple web service returns first n Fibonacci numbers
"""

import ConfigParser
import json
import logging
import os
import threading
import socket
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

LOG_FILE = "/var/log/fibwebservice.log"
CONFIG_FILE = "/etc/fibserver.cfg"
FAILURE = 1
SUCCESS = 0
VALID_PORT_RANGE = range(1024, 65535) 
VALID_OUTPUT_FORMAT = ['json', 'xml']
FIB_MAX = 10000
VALID_FIB_RANGE = range(1, FIB_MAX + 1)

global_configs = {}

def exit_with_msg(msg):
    """
    Print the specified message, and exit with failure
    """
    print msg
    sys.exit(FAILURE)

def get_configuration():
    """
    Return the global_configs to avoid using global everywhere.
    """
    global global_configs
    return global_configs

def default_configuration():
    """
    Generate default configuration
    """
    configs = get_configuration()
    configs["host"] = "localhost"
    configs["port"] = 8000
    configs["output_format"] = 'json'

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

def import_configuration(config_file):
    """
    Import basic configuration for conf file
    """
    configs = get_configuration()


    try:
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(config_file)
        configs["host"] = config_parser.get("Server", "host")
        configs["port"] = config_parser.getint("Server", "port")
        configs["output_format"] = config_parser.get("Output", "format")
    except ConfigParser.Error:
        print "Error during loading configuration file. Use default configuration"
        default_configuration()
 
    if not is_port_valid(configs["port"]):
        return FAILURE, "Invalid port %d" % configs["port"]
    if not is_output_format_valid(configs["output_format"]):
        return FAILURE, "Invalid output format %s" % configs["output_format"]

    return SUCCESS, None

def output_formatting(fib_list, output_format):
    """
    Convert the fib list into specified format
    """
    if output_format == "json":
        return json.dumps(fib_list)
    elif output_format == "xml":
        try:
            for i in range(0, len(fib_list)):
                fib_list[i] = str(fib_list[i])
            fib_str = str(" ").join(fib_list)
        except TypeError, msg:
            logging.error(msg)
            fib_str = ""
        xml_output = '<?xml version="1.0" encoding="UTF-8"?><fib>%s</fib>' % fib_str
        return xml_output
    else:
        # return json format as default
        return json.dumps(fib_list)
    return

def fibs(num):
    """
    Return the fib list with specified number
    """
    
    if num not in VALID_FIB_RANGE:
        return []

    if num == 1:
        return [0]
    else:
        result = [0, 1]
        for i in range(num-2):
            result.append(result[-2]+result[-1])
        return result

class httpServHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler
    """
    def do_GET(self):
        """
        GET
        """

        fib_num, is_valid = self.validate_request()
 
        if is_valid:
            configs = get_configuration()
            self.send_response(200)
            self.send_header('Content-type', 'text/%s' % configs['output_format'])
            self.end_headers()
            result = fibs(fib_num)
            self.wfile.write(output_formatting(result, configs['output_format']))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("The request url must be a postive integer number between 1 and %d" % FIB_MAX)
        

        #print threading.currentThread().getName()

    def log_message(self, format, *args):
        """
        log the message of the web service
        """
        logging.info(format % args)

    def validate_request(self):
        """
        Chech if the request is in a valid format
        """
        if self.path.find('?') != -1:
            self.path, self.query_string = self.path.split('?', 1)
        else:
            self.query_string = ''

        # get the fib number from the url
        fib_num = 0
        if self.path.find('/') != -1:
            fib_num = self.path.split('/')[-1]

        # bypass the favicon for browser
        if fib_num == "favicon.ico":
            return 0, False

        # bad request for non-integer
        try:
            fib_num = long(fib_num)
        except ValueError:
            return 0, False

        # bad request for negative value
        if fib_num not in VALID_FIB_RANGE:
            return 0, False

        return fib_num, True
           

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Handle requests in a separate  thread.
    """
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
    configs = get_configuration()

    try:
        server_address = (configs['host'], configs['port'])
        server = ThreadedHTTPServer(server_address, httpServHandler)
        print "Starting server, useg <Ctrl-C> to stop"
    except socket.error, msg:
        exit_with_msg(msg)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down the server..."
        server.shutdown()

if __name__ == "__main__":
    try:
        run()
    except Exception, msg:
        # leave no exceptions to the user.
        exit_with_msg(msg)

