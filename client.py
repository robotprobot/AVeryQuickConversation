import socket
import threading

# Get user to choose nickname
nickname = input("Enter your nickname: ")

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receivemessages():
    while True:
        try:
            # Receive the message from the server
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                # Send the nickname to the server
                client.send(nickname.encode('ascii'))
            else:
                # Print the message
                print(message)
        except:
            # Disconnect the client upon error
            print("Disconnected from server.")
            client.close()
            break

def sendmessages():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

ReceiveThread = threading.Thread(target=receivemessages)
ReceiveThread.start()

SendThread = threading.Thread(target=sendmessages)
SendThread.start()