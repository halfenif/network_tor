import sys
import io
import pycurl
import stem.process
from stem.util import term

import time
import socket
import os
constDataFolder = './data_tor/'

def get_socket_port():
    SOCKS_PORT_START = 7000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                     #2 Second Timeout

    result = 0
    while(result == 0):
        result = sock.connect_ex(('127.0.0.1',SOCKS_PORT_START))
        if result == 0:
            SOCKS_PORT_START = SOCKS_PORT_START + 1
        else:
            print('SOCKS_PORT:', SOCKS_PORT_START)
            return SOCKS_PORT_START

def query(url, socket_port):
    print('-------------------------------------------------------------------')
    """
    Uses ptcurl to fetch a site using the proxy on the SOCKS_PORT
    """

    output = io.BytesIO()

    query = pycurl.Curl()
    query.setopt(pycurl.URL, url)
    query.setopt(pycurl.PROXY, 'localhost')
    query.setopt(pycurl.PROXYPORT, socket_port)
    query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    query.setopt(pycurl.WRITEFUNCTION, output.write)

    try:
        #print('Before - query.perform()')
        time_start = time.time()
        query.perform()
        print('QueryTime:', round(time.time() - time_start), 'sec')
        #print('After - query.perform()')

        #print(output.getvalue().decode('utf-8','ignore').encode("utf-8"))
        print(output.getvalue().decode('utf-8','ignore'))
        return ""
    except pycurl.error as exc:
        return "Unable to reach %s (%s)" % (url, exc)


def tor_process(url, socket_port):
    str_socket_port = str(socket_port)
    strDataFolder = constDataFolder + str_socket_port
    try:
        os.stat(strDataFolder)
    except:
        os.makedirs(strDataFolder)

    tor_process = stem.process.launch_tor_with_config(
        config = {
            #'tor_cmd':"C:/Users/junye/Desktop/Tor Browser/Browser/TorBrowser/Tor/Tor.exe",
            'SocksPort':str_socket_port,
            'DataDirectory':strDataFolder,
            #'ExitNodes':'{ru}',
        },
        init_msg_handler = print_bootstarp_lines,
    )

    try:
        query(url, socket_port)
    finally:
        tor_process.kill() #stops tor

#Start as instance of Tor configured to only exit through (ru)Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running

def print_bootstarp_lines(line):
    print("line:" + line)
    if "Bootstrapped" in line:
        #print(term.format(line, term.Color.BLUE))
        #print(line)
        pass


#---------------------------------
# Main
if __name__ == "__main__":
    socket_port = get_socket_port()
    #print(term.format("Starting Tor:\n", term.Attr.BOLD))
    #print("Starting Tor:")
    url = "https://www.atagar.com/echo.php"
    url = "https://www.google.com"
    #url = "https://www.clien.net/service/board/park/10843228"
    while(True):
        tor_process(url, socket_port)

    #print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
    #print("Checking our endpoint:")
