import sys
import socket
import threading
import PySimpleGUI as gui

# Declare variables and setup socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Receiving thread
def receivemessages(nickname):
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
            gui.popup("Disconnected from the server.", title="Disconnected", button_color=("white", "red"))
            connect_gui()

# Sending thread
def sendmessages(nickname):
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Render the main GUI
def main_gui():
    layout = [[], []]
    window = gui.Window("AVeryQuickConversation", layout)
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            window.close()
            break

# Render the connection GUI
def connect_gui():
    layout = [[gui.Text("Welcome! Please enter the details of the server you want to connect to.")], [gui.Text('IP:', 8,1), gui.InputText("127.0.0.1")], [gui.Text('Port:', 8,1), gui.InputText("55555")], [gui.Text('Username:', 8,1), gui.InputText("steven")], [gui.Button("Connect")]]
    window = gui.Window("AVeryQuickConversation", layout)
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            window.close()
            break
        if event == "Connect":
            connectionIP = values[0]
            connectionPort = int(values[1])
            nickname = values[2]
            
            if connectionIP == "" or connectionPort == "" or nickname == "":
                gui.popup("Please enter all the details.", title="Missing details", button_color=("white", "red"))
            else:
                try:
                    # Connect to the server
                    client.connect((connectionIP, connectionPort))
                    # Start the receiving thread
                    threading.Thread(target=receivemessages, args=(nickname,)).start()
                    # Start the sending thread
                    threading.Thread(target=sendmessages, args=(nickname,)).start()
                    # Close the connection GUI
                    window.close()
                    # Call the main GUI
                    main_gui()
                except:
                    gui.popup("Could not connect to the server at " + connectionIP + ".", title="Connection error", button_color=("white", "red"))

# Call the connection GUI
connect_gui()