# todo: create a TCP socket 
# todo: bind it to server address 
# todo: then listen for upcoming connection

import socket
from threading import Thread

# server IP address
SERVER_IP = '0.0.0.0' # All ipv4 addresses on machine
SERVER_PORT = 5080 
seperator_token = "<SEP>" # use to seperate the client name and message

# initialize list/set of all connected clients  socket
client_sockets = set()

# create a TCP socket 
s = socket.socket()

# make port reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to server 
s.bind((SERVER_IP, SERVER_PORT))

# listen for upcoming connection
s.listen(5)

print(f"[*]Listening as {SERVER_IP}: {SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:

        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected 
            # remove it form set
            print(f"[!]ERROR: {e}")
            client_sockets.remove(cs)

        else:
            # if we recieved a message, replace <SEP> 
            # token with ": " for nice printng
            msg = msg.replace(seperator_token, ": ")

        # irterate over all connected sockets
        for client_sock in client_sockets:
            # and send message
            client_sock.send(msg.encode())

while True:
    # keep listening for connections all the time
    client_socket, client_address = s.accept()
    print(f"[+]{client_address}: Connected.")

    # add the new connected client to the sockets
    client_sockets.add(client_socket)

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon= True

    # start the thread
    t.start()


for cs in client_sockets:
    cs.close()

s.close()