#import required modules

import socket
import threading


HOST = '127.0.0.1'
PORT = 1235 # You can use any port between 0 to 65535

def listen_for_messages_from_server(client):
    
    while 1:
        message=client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split("~")[1]
            
            print(f"[{username}] : {content}")
        else:
            print("Message recieved from client is empty")
        
def send_message_to_server(client):
    while 1:
        message = input("Message : ")
        if(message != ""):
            client.sendall(message.encode())
        else:
            print("Empty Message")
            exit(0)

def communicate_to_server(client):
    username = input("Enter Username : ")
    if(username!=""):
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)

    #!thread
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    
    send_message_to_server(client)

def main():
    #creating socket object
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #connect to the server
    try:
        client.connect((HOST,PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} and {PORT}")
    
    communicate_to_server(client)
if __name__ == '__main__':
    main()