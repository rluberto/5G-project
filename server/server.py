import socket
import random

try:
    while True:
        # Establish the server and allow for client connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 1002))
        server.listen()
        client_socket, client_address = server.accept()

        # Create a new file to write the image to
        file = open('media/'+str(random.randint(100000, 999999))+'_image.jpg', "wb")

        # Write all of the data received from the client to the image file
        image_chunk = client_socket.recv(2048)
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048)
            print(image_chunk.__len__())
        # ---- record recvd time
        file.close()
        client_socket.close()

        # ---- get sent time from client
        # ---- calc elapsed time (latency) recvd - sent
        # ---- calc bandwidth recvd_file_size/latency
        # ---- store results

# Exit the program if the keyboard interrupt is datected
except KeyboardInterrupt:
    exit()
