import socket
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1002))
server.listen()

client_socket, client_address = server.accept()


file = open('media/'+str(random.randint(100000, 999999))+'_image.jpg', "wb")
image_chunk = client_socket.recv(2048)

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)

file.close()
client_socket.close()
