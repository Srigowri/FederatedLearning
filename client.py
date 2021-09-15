import socket
import pickle 
sock = socket.socket()
ipaddress = "localhost"
port = 3000
sock.connect((ipaddress,port))
print("Connected to server")
message_to_server = "hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1,hello this is client1"
message_to_server = pickle.dumps(message_to_server)
sock.sendall(message_to_server)
print("Sent the ML model back")

server_message = b""
bufsize = 32
while True:
    data = sock.recv(bufsize)
    server_message += data
    if not data:
        break
    if str(data)[-2]=='.':
        server_message = pickle.loads(server_message)
        break
print("Client program server message",server_message)
print("---------------")

message_to_server1 = "abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz,abcdefghijklmonpqrstuvwxyz"
message_to_server1 = pickle.dumps(message_to_server1)
sock.sendall(message_to_server1)
print("Sent the ML model back")




sock.close()
print("Socket closed")



