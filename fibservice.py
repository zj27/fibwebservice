#!/usr/bin/python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import json
import socket
import sys
import ConfigParser

CONFIG_FILE = "/etc/fibserver.cfg"
FAILURE = 1
VALID_PORT_RANGE = range(1024, 65535) 
VALID_OUTPUT_FORMAT = ['json']

global_configs = {}


def get_configuration():
    """
    Return the global_configs to avoid using global everywhere.
    """
    global global_configs
    return global_configs

def default_configuration():
    configs = get_configuration()
    configs["host"] = "localhost"
    configs["port"] = 8000
    configs["output_format"] = 'json'

def is_port_valid(port):
    if port in VALID_PORT_RANGE:
        return True
    else:
        return False

def is_output_format_valid(output_format):
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
        print "Invalid port %d" % configs["port"] 
        sys.exit(FAILURE)
    if not is_output_format_valid(configs["output_format"]):
        print "Invalid output format %s" % configs["output_format"]
        sys.exit(FAILURE)

def output_formatting(fib_list, output_format):
    """
    Convert the fib list into specified format
    """
    # So far we only support json format which is best for Fibonacci numbers.
    # Keep the function here just for future expansion.
    if output_format == "json":
        return json.dumps(fib_list)
    else:
        # return json format as default
        return json.dumps(fib_list)
    return

def fibs(num):
    """
    Return the fib list with specified number
    """
    if num <= 0:
        return []
    elif num == 1:
        return [0]
    else:
        result = [0, 1]
        for i in range(num-2):
            result.append(result[-2]+result[-1])
        return result

class httpServHandler(BaseHTTPRequestHandler):
    def do_GET(self):

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
            self.wfile.write("The request url must be a postive integer number")
        

        #print threading.currentThread().getName()

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
            fib_num = int(fib_num)
        except ValueError:
            return 0, False

        # bad request for negative value
        if fib_num < 0:
            return 0, False

        return fib_num, True
           

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Handle requests in a separate  thread.
    """

def run():
    """
    Main function to run the web service
    """

    import_configuration(CONFIG_FILE)
    configs = get_configuration()

    try:
        server_address = (configs['host'], configs['port'])
        server = ThreadedHTTPServer(server_address, httpServHandler)
        print "Starting server, useg <Ctrl-C> to stop"
    except socket.error, msg:
        print msg
        sys.exit(FAILURE)

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
        print msg
        sys.exit(FAILURE)

