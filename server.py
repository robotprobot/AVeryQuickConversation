from datetime import datetime
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = None

clients = []
clientnicknames = []

def connect():
    # Start the server
    server.bind((host, int(port)))
    server.listen(0)
    print("AVeryQuickConversation server started.")
    acceptclients()

def broadcastmessage(message):
    # Send the message to all clients
    for client in clients:
        client.send(message)

def handleclient(client):
    while True:
        try:
            # Receive the message from the client
            message = client.recv(1024)
            if message:
                broadcastmessage(message)
        except:
            # Disconnect the client
            index = clients.index(client)
            clients.remove(client)
            clients.close()
            clientnickname = clientnicknames[index]
            broadcastmessage(datetime.now() + ": {} disconnected from the chat server.".format(clientnickname).encode('ascii'))
            clientnicknames.remove(clientnickname)
            break

def acceptclients():
    while True:
        # Accept a connection from a client
        client, address = server.accept()
        
        # Request and receive the nickname of the client
        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clientnicknames.append(nickname)
        clients.append(client)
        broadcastmessage(datetime.now() + ": {} connected to the chat server.".format(nickname).encode('ascii'))

        # Create a thread to handle the client
        thread = threading.Thread(target=handleclient, args=(client,))
        thread.start()

port = input("Enter port to listen on: ")
connect()