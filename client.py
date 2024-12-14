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
SERVER_PORT = 5080 # servers port
separator_token = "<SEP>" # use this to seperate client name and message

# initialize TCP socket
s = socket.socket()
print(f"[*]Connecting to {SERVER_HOST}: {SERVER_PORT}")

# connect to server
s.connect((SERVER_HOST, SERVER_PORT))
print(f"[+]Connected.")

# prompt client for a name
name = input("Enter Your name: ")

def listen_for_messages():
    """Listens for messages comming from server"""
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client and prints them
t = Thread(target=listen_for_messages)  
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

    # add date time and color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"

    # send the message
    s.send(to_send.encode())

# close the socket
s.close()