import socket
import time
import pickle

# Establish a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

# Open the image file that is going to be transferred
file_path = 'media/image2.jpg'
file = open(file_path, 'rb')

# Create a send time array
send_time_array = []

# Write all of the image data to the server
image_data = file.read(2048)
while image_data:
    send_time_array.append(time.time())
    client.send(image_data)
    image_data = file.read(2048)
file.close()
client.close()


# Establish a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))

data = pickle.dumps(send_time_array)
client.sendall(data)

client.close()