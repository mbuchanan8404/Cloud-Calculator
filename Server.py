# Matthew Buchanan
# Networking and Data Structures
# Spring 2019
# Project 1: udp client and server with threaded reliable connections to clients

from RequestHandler import requestHandler
from socket import *
import threading
import sys


# This function is a thread that maintains state/connection for a client
def establishConnection(mes, add):
    calculatorOn = False
    newProxySocket = socket(AF_INET, SOCK_DGRAM)  # Create a new port for the connection
    newProxySocket.sendto(mes, add)  # Send client back client's message
    proxyAddress = newProxySocket.getsockname()[1]
    newProxySocket.sendto(str(proxyAddress).encode(), add)  # Send the new port number to the client

    # Listen until user ends connection
    while True:
        currentMessage = newProxySocket.recvfrom(2048)[0]

        # Perform 3 way hand shake protocol
        verificationResponse1 = ""
        while verificationResponse1 != "311":
            newProxySocket.sendto(currentMessage, add)
            verificationResponse1 = newProxySocket.recvfrom(2048)[0]
            verificationResponse1 = verificationResponse1.decode()

        answer, calculatorOn = requestHandler(currentMessage.decode(), calculatorOn, add)

        # Perform 3 way hand shake protocol
        verificationResponse2 = "411"
        newProxySocket.sendto(answer.encode(), add)
        while answer.encode() != newProxySocket.recvfrom(2048)[0]:
            newProxySocket.sendto(answer.encode(), add)
        newProxySocket.sendto(verificationResponse2.encode(), add)

        if answer[0:8] == "200  BYE":
            return  # kill the thread



# "main" program begins here, a server is set up and bound to a port #
if len(sys.argv) != 2:
    print("Wrong number of command line arguments")
    exit()

serverPort = int(sys.argv[1])
print("Server Started")
mainServerSocket = socket(AF_INET, SOCK_DGRAM)  # ipv4, datagram
mainServerSocket.bind( ("0.0.0.0", serverPort) )

while True:
    clientMessage, clientAddress = mainServerSocket.recvfrom(2048)
    if clientMessage.decode() == "HELO":  # HELO is sent by each new client before the user is even aware
        clientMessage = "200"
        # Create a thread to represent a client and maintain a connection despite using udp
        newClient = threading.Thread(target=establishConnection, args=(clientMessage.encode(), clientAddress))
        newClient.start()
        print("New Client " + str(clientAddress[0]) + " (UDP)")



