# Matthew Buchanan
# Networking and Data Structures
# Spring 2019
# Project 1: udp client and server with threaded reliable connections to clients

from socket import *
import sys

# Set server variables and establish a connection/get a proxy server port
# Reliable udp server/client project with 3-way handshake protocol connections for all IO
if len(sys.argv) != 3:
    print("Wrong number of command line arguments")
    exit()

serverHostName = str(sys.argv[1])
serverPort = int(sys.argv[2])
connectionRequestCode = "HELO"
connectionAcceptedCode = "200"

# Establish connection with server
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.sendto(connectionRequestCode.encode(), (serverHostName, serverPort) )  # Part one of establishing a connection, send connection request
response, serverAddress = clientSocket.recvfrom(2048)
if response.decode() == connectionAcceptedCode:  # Part two, check for correct code from server
    response, serverAddress = clientSocket.recvfrom(2048)
    serverPort = int(response.decode())  # Part three, reassign server port to proxy provided by server

# Run the program until user enters BYE
while True:
    verificationResponse = "311"
    userInput = input("Please enter a command for the Cloud Calculator:\n")
    clientSocket.sendto(userInput.encode(), (serverHostName, serverPort))

    # Perform three way handshake protocol
    while userInput.encode() != clientSocket.recvfrom(2048)[0]:
        clientSocket.sendto(userInput.encode(), (serverHostName, serverPort))
    clientSocket.sendto(verificationResponse.encode(), (serverHostName, serverPort))

    message = clientSocket.recvfrom(2048)[0]
    # Perform 3 way hand shake protocol
    verificationResponse = ""
    while verificationResponse != "411":
        clientSocket.sendto(message, (serverHostName, serverPort))
        verificationResponse = clientSocket.recvfrom(2048)[0]
        verificationResponse = verificationResponse.decode()

    if message.decode()[0:8] == "200  BYE":
        print(message.decode())
        exit()
    print(message.decode())
