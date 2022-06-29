import socket
import threading

host = '127.0.0.1'
port = 55555

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(0)

clients = []
clientnicknames = []

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
            broadcastmessage('{} left the chat.'.format(clientnickname).encode('ascii'))
            clientnicknames.remove(clientnickname)
            break

def connectclient():
    while True:
        # Accept a connection from a client
        client, address = server.accept()
        
        # Request and receive the nickname of the client
        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clientnicknames.append(nickname)
        clients.append(client)
        broadcastmessage("{} joined the chat.".format(nickname).encode('ascii'))

        # Create a thread to handle the client
        thread = threading.Thread(target=handleclient, args=(client,))
        thread.start()

print("Server started.")
connectclient()