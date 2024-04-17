import socket
import threading
import random
import pickle
import time
import json
import sys
import os
import select

# Define the server hostname or IP address
SERVER_HOSTNAME = sys.argv[1]

receive_time_array = []
sent_time_array = []
file_metadata = []
transferred_data_length_array = []
receive_data_ready = False
send_data_ready = False
file_number = ''
ready_to_stop_server = False

def handle_connection(client_socket, port):
    global receive_time_array
    global sent_time_array
    global file_metadata
    global receive_data_ready
    global send_data_ready
    global file_number
    global ready_to_stop_server

    # Transfer the image from the client to the server
    if port == 8000: # Used for receiving images
        print("Received connection on port 8000")
        file_number = sys.argv[2]
        file = open('media/'+file_number+'_media', "wb")
        receive_time_array.clear()
        transferred_data_length_array.clear()
        image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
        receive_time_array.append(time.time_ns())
        transferred_data_length_array.append(image_chunk.__len__())
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
            if image_chunk.__len__() != 0:
                receive_time_array.append(time.time_ns())
                transferred_data_length_array.append(image_chunk.__len__())
        file.close()
        receive_data_ready = True

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
        send_data_ready = True

    # Perform calculations based on the send time and receive time data
    if receive_data_ready and send_data_ready:
        # After the image has been transferred and the image metadata is received, rename the file to include the file extension
        file_extension = str(file_metadata[0])
        os.rename('media/'+file_number+'_media', 'media/'+file_number+'_media.'+file_extension)
        #Create an empty latency and bandwidth array
        latency_array = []
        bandwidth_array = []
        # Calculate the latency and bandwidth for "data chunk" that was transferred
        if(len(receive_time_array) == len(sent_time_array)):
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
        with open('benchmark-data/'+file_number+'_benchmark.json', 'w') as json_file:
            json.dump(benchmark_data, json_file)
        print("File saved as: "+file_number+"_media."+file_extension)
        print("Benchmark data saved as: "+file_number+"_benchmark.json")    
        receive_data_ready = False
        send_data_ready = False
        ready_to_stop_server = True
    client_socket.close()


def start_server(port):
    global ready_to_stop_server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOSTNAME, port))
    server_socket.listen(5)
    server_socket.setblocking(0)  # Set socket to non-blocking mode
    print(f"Listening on port {port}...")

    while True:
        ready_to_read, _, _ = select.select([server_socket], [], [], 0)
        if ready_to_read:
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address[0]}:{address[1]} on port {port}")
            threading.Thread(target=handle_connection, args=(client_socket, port)).start()
        elif ready_to_stop_server:
            print("Stopping server...")
            server_socket.close()
            break

# Start servers on multiple ports
threading.Thread(target=start_server, args=(8000,)).start()
threading.Thread(target=start_server, args=(9000,)).start()