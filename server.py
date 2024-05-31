#importing

import socket #used for main communication part
import threading #used to run the component thread

HOST = '127.0.0.1'
PORT = 1235 # You can use any port between 0 to 65535
LISTENER_LIMIT=500
active_clients = []

#function to listen for upcoming messages from a client
def listen_for_messages(client,username):
    
    while 1:
        
        message = client.recv(2048).decode('utf-8')
        if( message==""):
            print(f"Message sent from client {username} is empty")
        else:
            final_msg = username + '~' + message
            send_message_to_all(final_msg)



#function to send message to single client
def send_message_to_client(client,message):
    client.sendall(message.encode())
    
    
#function to send any new message to all the client that are currently connected to the server
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message )
        

#Function to handle client
def client_handler(client):
    # Server-will listen for client message that will
    #- Contain- the username
    while 1:
        username = client.recv(2048).decode("utf-8")
        if username == "":
            print("Client username is empty")
        else:
            active_clients.append((username,client))
            prompt_message = 'SERVER ~' + f'{username} added to the chat'
            send_message_to_all(prompt_message)
            break
        
        
    #!threading
    threading.Thread(target=listen_for_messages,args=(client,username, )).start()
            



#Main function
def main():
    #createing the socket class objet
    #AF_INET: •we-are going to use IPv4 addresses
    #- SOCK_STREAM: we are using TCP packets for communication for udp:socket.SOCK_DGRAM
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    #creating try catch
    try:
        server.bind((HOST,PORT))
        print("Server is running")
    except:
        print(f"Unable to bind to Host {HOST} and port {PORT}")
        
    #set server limit
    server.listen(LISTENER_LIMIT)
    
    #it will keep listen client conection
    while 1:
        client,address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        
        #!Threading
        threading.Thread(target=client_handler, args=(client, )).start()
        
        
        
if __name__ == '__main__':
    main()
