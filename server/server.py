import socket
import threading
import random
import pickle
import time
import matplotlib.pyplot as plt
import numpy as np
import json

receive_time_array = []
sent_time_array = []
rta_processing_done = False
sta_processing_done = False
file_random_number = ''

def handle_connection(client_socket, port):
    global receive_time_array
    global sent_time_array
    global rta_processing_done
    global sta_processing_done
    global file_random_number

    # Transfer the image from the client to the server
    if port == 8000: # Used for receiving images
        print("Received connection on port 8000")
        file_random_number = str(random.randint(100000, 999999))
        file = open('media/'+file_random_number+'_media.jpg', "wb")
        receive_time_array.clear()
        image_chunk = client_socket.recv(2048)
        receive_time_array.append(time.time())
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048)
            if image_chunk.__len__() != 0:
                receive_time_array.append(time.time())
        file.close()
        print('RTA: ' + str(len(receive_time_array)))
        rta_processing_done = True

    # Transfer the send time data from the client to the server
    elif port == 9000: # Used for getting benchmark data
        print("Received connection on port 9000")
        sent_time_array.clear()
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        sent_time_array = pickle.loads(data)
        print('STA: ' + str(len(sent_time_array)))
        sta_processing_done = True

    # Perform calculations based on the send time and receive time data
    if rta_processing_done and sta_processing_done: # Calculate latency after both send and received arrays are complete
        print("Latency Array: ")
        latency_array = []
        for i in range(len(receive_time_array)):
            latency = receive_time_array[i] - sent_time_array[i]
            latency_array.append(latency)
        print(latency_array)
        # Print the benchmark arrays to a json file
        benchmark_data = {
            "sent_time_array": sent_time_array,
            "receive_time_array": receive_time_array,
            "latency_array": latency_array
        }
        with open('benchmark-data/'+file_random_number+'_benchmark.json', 'w') as json_file:
            json.dump(benchmark_data, json_file)
        rta_processing_done = False
        sta_processing_done = False

    client_socket.close()


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address[0]}:{address[1]} on port {port}")
        threading.Thread(target=handle_connection, args=(client_socket, port)).start()

# Start servers on multiple ports
threading.Thread(target=start_server, args=(8000,)).start()
threading.Thread(target=start_server, args=(9000,)).start()