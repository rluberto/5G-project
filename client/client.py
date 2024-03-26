import socket
import time
import os
from csv import writer

# Establish a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1002))

# Open the image file that is going to be transferred
file_path = 'media/image.JPG'
file = open(file_path, 'rb')

# Write all of the image data to the server
image_data = file.read(2048)
start_time = time.time() # Record the start time (used to calculate latench and bandwidth)
while image_data:
    client.send(image_data)
    image_data = file.read(2048)
stop_time = time.time() # Record the stop time (used to calculate latench and bandwidth)
# ---- record sent time
file.close()
client.close()

# ---- send sent time

# Collect latency and bandwidth benchmark data
latency = stop_time - start_time
file_size = os.path.getsize(file_path)
bandwidth = file_size/latency
print("Latency:", latency, "seconds")
print("Bandwidth:", bandwidth, "bytes/second")

# Append latency and bandwidth benchmark data to a csv file
data_file_name = 'local_benchmarks.csv'
csv_append_data = [latency, bandwidth]
with open(data_file_name, 'a') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(csv_append_data)
    f_object.close()
