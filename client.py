# imports threading, socket, and sys libraries

import threading
import socket


# This receives the user input
alias = input('Input username >>> ')

# here we created client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))



def client_receive():

    while True:

        try:
            message = client.recv(1024).decode('utf-8')

            if message == "alias?":

                client.send(alias.encode('utf-8'))

            else:
                print(message)

        except:

            a_d = str(alias)
            print(f'{a_d} has left the room!')
            client.close()
            break


# Here we check if a user exited the chat. If so, then the server removes that specific user
def client_send():

    while True:

        message = f'{alias}: {input("")}'

        if ".exit" in str(message):

            client.send(message.encode('utf-8'))
            break

        else:

            client.send(message.encode('utf-8'))

    client.close()


# this section deals with threading
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
