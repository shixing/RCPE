'''
possible fields are name, city and full_addr
they should be spelt exactly the same
just follow the format in main


must - must contain
mustnot - must not contain
should - default option
they also should be spelt exactly the same and can't be missed
'''
__author__ = 'Ai He'
from socket import *
import json
import time

def getBusiness(jsonQuery):
    HOST = 'sava.usc.edu'
    #HOST = 'localhost'
    PORT = 12345
    BUFFERSIZE = 1024
    ADDR = HOST, PORT
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect(ADDR)
    tcpSocket.send(jsonQuery)
    tcpSocket.send('\n')
    tcpSocket.send('###\n')
    print jsonQuery
    time.sleep(2)
    #tcpSocket.settimeout(2)
    data = tcpSocket.recv(1024*1024)
    print data
    tcpSocket.close()

if __name__ == '__main__':
    #j = json.loads('{"name":["tax service", "must"], "state":["CA", "mustnot"], "type":["business", "should"]}')
    #getBusiness('{"business":{"name":["tax service", "must"], "city":["Chandler", "should"], "type":["business", "should"]}}')
    getBusiness('{"rcpair":{"reason":["good place", "must"]}}')
