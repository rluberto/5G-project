import socket
import time
import pickle
import sys

# Define the server hostname or IP address
SERVER_HOSTNAME = sys.argv[1]

# Open the image file that is going to be transferred
file_path = sys.argv[2]
file = open(file_path, 'rb')

# Initialize the send time array and file metadata array
send_time_array_ns = []
file_metadata_array = [file_path.split('.')[-1]]

# **** File Transfer Section ****
# Establish a socket connection for sending the image
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOSTNAME, 8000))

# Write all of the image data to the server
image_data = file.read(2048)
while image_data:
    send_time_array_ns.append(time.time_ns())
    client.send(image_data)
    image_data = file.read(2048)
file.close()
client.close()

# **** Metadata Transfer Section ****
# Establish a socket connection for sending benchmark data
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOSTNAME, 9000))

# Send the send time array and file metadata to the server
send_time_data_ns = pickle.dumps((send_time_array_ns, file_metadata_array))
client.sendall(send_time_data_ns)
# Close the client connection
client.close()