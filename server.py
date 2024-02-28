# imports threading, socket, and sys libraries

import threading
import socket
import sys

# Creates the localhost ip and port, assigns to the server, and uses an empty list for the clients and aliases variables
host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []



# This function broadcast messages to the client
def broadcast(message):
    for client in clients:
        client.send(message)

# This function handles clients' connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            #exiting client
            print(f'Client: {client} and Client List: {clients}')
            if ".exit" in str(message):
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                a_d = alias.decode('utf-8')
                msg_de = message.decode('utf-8')
                broadcast(f'{a_d} has left the chat room! with message {msg_de}'.encode('utf-8'))
                aliases.remove(alias)
                break
            else:
                broadcast(message)
        except:

            print(f'Error Occurred! {sys.exc_info()[0]}')
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break



# This function receives the clients connection
def receive():

    while True:

        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        a_d = alias.decode('utf-8')
        output = f'The alias of this client is {a_d}'.encode('utf-8')
        # This cleans up the unwanted b' in the output
        print(output.decode('utf-8'))
        broadcast(f'{a_d} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



if __name__ == "__main__":

    receive()
