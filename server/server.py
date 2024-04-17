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

receive_time_array_ns = []
sent_time_array_ns = []
file_metadata = []
transferred_data_length_array_bytes = []
receive_data_ready = False
send_data_ready = False
file_number = ''
ready_to_stop_server = False

def handle_connection(client_socket, port):
    global receive_time_array_ns
    global sent_time_array_ns
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
        receive_time_array_ns.clear()
        transferred_data_length_array_bytes.clear()
        image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
        receive_time_array_ns.append(time.time_ns())
        transferred_data_length_array_bytes.append(image_chunk.__len__())
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
            if image_chunk.__len__() != 0:
                receive_time_array_ns.append(time.time_ns())
                transferred_data_length_array_bytes.append(image_chunk.__len__())
        file.close()
        receive_data_ready = True

    # Transfer the send time data from the client to the server
    elif port == 9000: # Used for getting benchmark data
        print("Received connection on port 9000")
        sent_time_array_ns.clear()
        file_metadata.clear()
        # Use pickle to load the data from the client
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        pickle_data = pickle.loads(data)
        # Unpack the send_time_array and file metedata from the pickle data
        sent_time_array_ns = pickle_data[0]
        file_metadata = pickle_data[1]
        send_data_ready = True

    # Perform calculations based on the send time and receive time data
    if receive_data_ready and send_data_ready:
        # After the image has been transferred and the image metadata is received, rename the file to include the file extension
        file_extension = str(file_metadata[0])
        os.rename('media/'+file_number+'_media', 'media/'+file_number+'_media.'+file_extension)
        # Create empty arrays for send time, receive time, adn transferred data length
        receive_time_array_ms = []
        send_time_array_ms = []
        receive_time_array_seconds = []
        send_time_array_seconds = []
        transferred_data_length_array_bits = []
        # Create empty arrays for latency and bandwidth
        latency_array_ns = []
        latency_array_ms = []
        latency_array_seconds = []
        bandwidth_array_bits_per_second = []
        # Calculate the latency and bandwidth for "data chunk" that was transferred
        if(len(receive_time_array_ns) == len(sent_time_array_ns)):
            # Convert units for time and transferred data length
            for i in range(len(receive_time_array_ns)):
                send_time_array_ms.append(sent_time_array_ns[i] / 1e6)
                receive_time_array_ms.append(receive_time_array_ns[i] / 1e6)
                send_time_array_seconds.append(sent_time_array_ns[i] / 1e9)
                receive_time_array_seconds.append(receive_time_array_ns[i] / 1e9)
                #Convert the transferred data length from bytes to bits
                transferred_data_length_array_bits.append(transferred_data_length_array_bytes[i] * 8)
            # Calculate the latency and bandwidth for each "data chunk" that was transferred
            for i in range(len(receive_time_array_ns)):
                # Calculae the latency in nanoseconds, milliseconds, and seconds
                latency_ns = receive_time_array_ns[i] - sent_time_array_ns[i]
                latency_ms = receive_time_array_ms[i] - send_time_array_ms[i]
                latency_seconds = receive_time_array_seconds[i] - send_time_array_seconds[i]
                # Append the latency in nanoseconds, milliseconds, and seconds to the latency arrays
                latency_array_ns.append(latency_ns)
                latency_array_ms.append(latency_ms)
                latency_array_seconds.append(latency_seconds)
                # Append the bandwidth in bits per second to the bandwidth array
                bandwidth_array_bits_per_second.append(transferred_data_length_array_bits[i] / latency_seconds)
        # Collect all of the benchmark data arrays
        benchmark_data = {
            # Transferred data length
            "transferred_data_length_array_bytes": transferred_data_length_array_bytes,
            "transferred_data_length_array_bits": transferred_data_length_array_bits,
            # Sent and received time
            "sent_time_array_ns": sent_time_array_ns,
            "receive_time_array_ns": receive_time_array_ns,
            "send_time_array_ms": send_time_array_ms,
            "receive_time_array_ms": receive_time_array_ms,
            "send_time_array_seconds": send_time_array_seconds,
            "receive_time_array_seconds": receive_time_array_seconds,
            # Latency
            "latency_array_ns": latency_array_ns,
            "latency_array_ms": latency_array_ms,
            "latency_array_seconds": latency_array_seconds,
            # Bandwidth
            "bandwidth_array_bits_per_second": bandwidth_array_bits_per_second
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