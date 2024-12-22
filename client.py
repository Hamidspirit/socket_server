# todo: connect to server 
# todo: keep listening for messages coming from server
# todo: wait for user input to send message

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# init colors
init()

# set the available colors 
colors = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# chose a random color for client
client_color = random.choice(colors)

# server's ip address
# if the server is not on this machine ,
# put the private (network) Ip address (e.g 192.168.1.2)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345 # servers port
separator_token = ": " # use this to seperate client name and message

# initialize TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[*]Connecting to {SERVER_HOST}: {SERVER_PORT}")


# prompt client for a name
name = input("Enter Your name: ")

def listen_for_messages(client_socket):
    """Listens for messages comming from server"""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("Disconnected")
            break

def start_client(SERVER_HOST, SERVER_PORT):
    """start the chat client"""
    client_socket = s

    # connect to server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[+]Connected.")

    # make a thread that listens for messages to this client and prints them
    t = Thread(target=listen_for_messages, args=(client_socket,))  
    # make the thread daemo so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:
        # input the message we eant to send to server
        to_send = input()

        # a way to exit the program
        if to_send.lower() == "q":
            break

        try:
            # add date time and color of the sender
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET} \n"
            # send the message
            s.send(to_send.encode('utf-8'))
        except:
            print("connection closed")

if __name__ == "__main__":
    start_client(SERVER_HOST, SERVER_PORT)