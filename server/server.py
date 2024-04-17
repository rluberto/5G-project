import socket
import threading
import pickle
import time
import json
import sys
import os
import select

# Define the server hostname or IP address
SERVER_HOSTNAME = sys.argv[1]

# Initialize global variables
receive_time_array_ns = []
send_time_array_ns = []
transferred_data_length_array_bytes = []
file_metadata = []
file_number = ''
receive_data_ready = False
send_data_ready = False
ready_to_stop_server = False

# Define the function to handle a connection to the server
def handle_connection(client_socket, port):
    # Define global variables in the handle_connection function
    global receive_time_array_ns
    global send_time_array_ns
    global file_metadata
    global receive_data_ready
    global send_data_ready
    global file_number
    global ready_to_stop_server

    # Transfer the image from the client to the server
    if port == 8000: # Port 8000 is used for receiving images
        print("Received connection on port 8000")
        # Ensure all global arrays are empty
        receive_time_array_ns.clear()
        transferred_data_length_array_bytes.clear()
        # Create a new file to store the file transferred from the client
        file_number = sys.argv[2]
        file = open('/home/'+os.getlogin()+'/5G-project/server/media/'+file_number+'_media', "wb")
        # Receive the file from the client and write it to the new file
        # This receives the file in 2048 byte chunks
        file_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
        receive_time_array_ns.append(time.time_ns())
        transferred_data_length_array_bytes.append(file_chunk.__len__())
        while file_chunk: # Continue to receive data until the file is completely transferred
            file.write(file_chunk)
            file_chunk = client_socket.recv(2048, socket.MSG_WAITALL)
            if file_chunk.__len__() != 0: # If the file chunk is not empty, append the receive time and transferred data length
                receive_time_array_ns.append(time.time_ns())
                transferred_data_length_array_bytes.append(file_chunk.__len__())
        file.close()
        receive_data_ready = True

    # Transfer the send time data and file metadata from the client to the server
    elif port == 9000: # Port 9000 is used for getting benchmark data
        print("Received connection on port 9000")
        # Ensure all global arrays are empty
        send_time_array_ns.clear()
        file_metadata.clear()
        # Use pickle to load the data from the client
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        pickle_data = pickle.loads(data)
        # Unpack the send_time_array and file metedata from the pickle data
        send_time_array_ns = pickle_data[0]
        file_metadata = pickle_data[1]
        send_data_ready = True

    # Perform calculations based on the send time and receive time data
    if receive_data_ready and send_data_ready:
        # After the image has been transferred and the image metadata is received, rename the file to include the file extension
        file_extension = str(file_metadata[0])
        os.rename('/home/'+os.getlogin()+'/5G-project/server/media/'+file_number+'_media', '/home/'+os.getlogin()+'/5G-project/server/media/'+file_number+'_media.'+file_extension)
        # Create empty arrays for send time, receive time, adn transferred data length
        transferred_data_length_array_bits = []
        # Calculate the latency and bandwidth for "data chunk" that was transferred
        if(len(receive_time_array_ns) == len(send_time_array_ns)):
            # Convert units for time and transferred data length
            for i in range(len(receive_time_array_ns)):
                #Convert the transferred data length from bytes to bits
                transferred_data_length_array_bits.append(transferred_data_length_array_bytes[i] * 8)
        # Collect all of the benchmark data arrays
        benchmark_data = {
            # Transferred data length
            "transferred_data_length_array_bits": transferred_data_length_array_bits,
            # Send and received time in nanoseconds
            "send_time_array_ns": send_time_array_ns,
            "receive_time_array_ns": receive_time_array_ns
        }
        # Save the benchmark data to a JSON file
        with open('/home/'+os.getlogin()+'/5G-project/server/benchmark-data/'+file_number+'_benchmark.json', 'w') as json_file:
            json.dump(benchmark_data, json_file)
        print("File saved as: "+file_number+"_media."+file_extension)
        print("Benchmark data saved as: "+file_number+"_benchmark.json")    
        receive_data_ready = False
        send_data_ready = False
        ready_to_stop_server = True
    client_socket.close()

# Define the function to start the server
def start_server(port):
    # Define global variables in the start_server function
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

# Use threading to start servers on multiple ports
threading.Thread(target=start_server, args=(8000,)).start()
threading.Thread(target=start_server, args=(9000,)).start()