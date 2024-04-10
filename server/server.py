import socket
import threading
import random
import pickle
import time
import json
import sys
import os

# Define the server hostname or IP address
SERVER_HOSTNAME = sys.argv[1]

receive_time_array = []
sent_time_array = []
file_metadata = []
transferred_data_length_array = []
rta_processing_done = False
sta_processing_done = False
file_random_number = ''

def handle_connection(client_socket, port):
    global receive_time_array
    global sent_time_array
    global file_metadata
    global rta_processing_done
    global sta_processing_done
    global file_random_number

    # Transfer the image from the client to the server
    if port == 8000: # Used for receiving images
        print("Received connection on port 8000")
        file_random_number = str(random.randint(100000, 999999))
        file = open('media/'+file_random_number+'_media', "wb")
        receive_time_array.clear()
        transferred_data_length_array.clear()
        image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
        receive_time_array.append(time.time())
        transferred_data_length_array.append(image_chunk.__len__())
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
            if image_chunk.__len__() != 0:
                receive_time_array.append(time.time())
                transferred_data_length_array.append(image_chunk.__len__())
        file.close()
        rta_processing_done = True

    # Transfer the send time data from the client to the server
    elif port == 9000: # Used for getting benchmark data
        print("Received connection on port 9000")
        sent_time_array.clear()
        file_metadata.clear()
        # Use pickle to load the data from the client
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        pickle_data = pickle.loads(data)
        # Unpack the send_time_array and file metedata from the pickle data
        sent_time_array = pickle_data[0]
        file_metadata = pickle_data[1]
        sta_processing_done = True

    # Perform calculations based on the send time and receive time data
    if rta_processing_done and sta_processing_done:
        # After the image has been transferred and the image metadata is received, rename the file to include the file extension
        file_extension = file_metadata[0]
        os.rename('media/'+file_random_number+'_media', 'media/'+file_random_number+'_media.'+file_extension)
        #Create an empty latency and bandwidth array
        latency_array = []
        bandwidth_array = []
        # Calculate the latency and bandwidth for "data chunk" that was transferred
        for i in range(len(receive_time_array)):
            latency = receive_time_array[i] - sent_time_array[i]
            latency_array.append(latency)
            bandwidth_array.append(transferred_data_length_array[i] / latency)
        # Collect all of the benchmark data arrays
        benchmark_data = {
            "transferred_data_length_array": transferred_data_length_array,
            "sent_time_array": sent_time_array,
            "receive_time_array": receive_time_array,
            "latency_array": latency_array,
            "bandwidth_array": bandwidth_array
        }
        # Save the benchmark data to a JSON file
        with open('benchmark-data/'+file_random_number+'_benchmark.json', 'w') as json_file:
            json.dump(benchmark_data, json_file)
        rta_processing_done = False
        sta_processing_done = False
    client_socket.close()


def start_server(port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOSTNAME, port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address[0]}:{address[1]} on port {port}")
        threading.Thread(target=handle_connection, args=(client_socket, port)).start()

# Start servers on multiple ports
threading.Thread(target=start_server, args=(8000,)).start()
threading.Thread(target=start_server, args=(9000,)).start()