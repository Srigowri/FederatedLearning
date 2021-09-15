"""
Server code
"""
import pickle #ML models are objects, used for encoding and decoding
import socket 


sock = socket.socket()  #create socket
print("Created Socket")
ipaddress,port = "localhost",10000   #bind the socket to IP address and port number 

#sock.bind(("192.168.1.4",10000))  #use ifconfig
sock.bind((ipaddress,port))
print("Socket is bound to the IP address: port number:",ipaddress, port)

sock.listen(1)  #listen to any incoming connection
print("Listening for incoming connection")

connected = False
accept_timeout = 30
sock.settimeout(accept_timeout)
try:
    connection, address = sock.accept()  #accept the incoming connection     
    connected = True 
except socket.timeout as e:
    print("Socket did not receive any connection",str(e))

if connected:
    print("Connected to client:",address)
    client_data = ""
    while True: #this loop terminates when the client closes the connection
        data = connection.recv(8)  #once connected, receive data from client 
        if not data:
            break
        client_data+=data
    
    print("Client data",client_data)
    client_data = pickle.loads(client_data)
    print("Server program client message",client_data)
    server_reply = "Hello client, I am the server"
    server_reply = pickle.dumps(server_reply)
    connection.sendall(server_reply)   

sock.close()
print("Socket is closing")


