"""
Server code with multi messages from client
"""
import pickle #ML models are objects, used for encoding and decoding
import socket 
import time 
import socket
import pickle
import time
import threading

class SocketThread(threading.Thread):
    
    def __init__(self, connection, client_info, bufsize=1024, timeout=5):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client_info = client_info
        self.bufsize = bufsize
        self.timeout = timeout

    def recv(self):
        #to receive multiple messages within the same connection 
        #no need to open and close client connections again and again
        start = time.time()
        client_data = b""
        data = b""
        while True: #this loop terminates when the client closes the connection
            try:
                data = self.connection.recv(self.bufsize)  #once connected, receive data from client 
                client_data +=data
                
                if data == b"": # Nothing received from the client.
                    client_data = b""
                    if (time.time() - start) > self.timeout:
                        return None, False 
                elif str(data)[-2]=='.':
                    #received all the message there is from client
                    if len(client_data)>0:
                        try:
                            client_data = pickle.loads(client_data)                        
                        except BaseException as e:
                            print("Error reading the client data"+str(e))                    
                        return client_data,True
                else:
                    start = time.time()
                
            except BaseException as e:
                print("Error receiving the client message"+str(e))
                return None,False    


    def run(self):
        while True: #this loop terminates when the client closes the connection
            time_struct = time.gmtime()
            print("Started receiving from \
                 {day}/{month}/{year} {hour}:{minute}:{second} GMT".format(year=time_struct.tm_year, 
                            month=time_struct.tm_mon, 
                            day=time_struct.tm_mday, 
                            hour=time_struct.tm_hour, 
                            minute=time_struct.tm_min, 
                            second=time_struct.tm_sec))      
            client_data,status = self.recv()
            print(client_data,status)
            
    
            if not status:
                self.connection.close()
                print("Closing connection with ",self.client_info)
                break
            server_reply = "Hello client, Received message"
            server_reply = pickle.dumps(server_reply)
            self.connection.sendall(server_reply) 




sock = socket.socket()  #create socket
print("Created Socket")
ipaddress,port = "localhost",3000   #bind the socket to IP address and port number 

#sock.bind(("192.168.1.4",10000))  #use ifconfig
sock.bind((ipaddress,port))
print("Socket is bound to the IP address: port number:",ipaddress, port)

sock.listen(1)  #listen to any incoming connection
print("Listening for incoming connection")


while True:
    try:
        connection, address = sock.accept()  #accept the incoming connection     

        print("New Connection from {client_info}.".format(client_info=address))
        socket_thread = SocketThread(connection=connection,
                                     client_info=address, 
                                     bufsize=1024,
                                     timeout=10)
        socket_thread.start()
        
        print("Connected to client:",address)

    except socket.timeout as e:
        print("Socket did not receive any connection",str(e))            
        sock.close()
        
        break