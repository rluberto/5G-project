import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Use command line arguement to get benchmark file number
benchmark_file_number = sys.argv[1]

# Load data from json file
data_file_path = 'benchmark-data/'+str(benchmark_file_number)+'_benchmark.json'
data = json.load(open(data_file_path))

# Extract data from json file
transferred_data_length_array_bits = data["transferred_data_length_array_bits"]
send_time_array_ns = data["send_time_array_ns"]
receive_time_array_ns = data["receive_time_array_ns"]

# Calculate latency
latency_array_ns = []
for i in range(len(send_time_array_ns)):
    latency_array_ns.append(receive_time_array_ns[i] - send_time_array_ns[i])

# Convert latency array from nanoseconds to milliseconds
latency_array_ms = []
for i in range(len(latency_array_ns)):
    latency_array_ms.append(latency_array_ns[i] / 1000000)

# Convert latency array from nanoseconds to seconds
latency_array_seconds = []
for i in range(len(latency_array_ns)):
    latency_array_seconds.append(latency_array_ns[i] / 1000000000)

# Calculate bandwidth bits/second
bandwidth_array_bits_per_second = []
for i in range(len(transferred_data_length_array_bits)):
    bandwidth_array_bits_per_second.append(transferred_data_length_array_bits[i] / latency_array_seconds[i])

# Calculate the running total of bits transferred
total_bits_transferred = []
for i in range(len(transferred_data_length_array_bits)):
    total_bits_transferred.append(sum(transferred_data_length_array_bits[:i+1]))

# Convert the receive time array from nanoseconds to milliseconds
receive_time_array_ms = []
for i in range(len(receive_time_array_ns)):
    receive_time_array_ms.append(receive_time_array_ns[i] / 1000000)

# Plot the Latecy vs Total Bits Transferred
xpoints = np.array(total_bits_transferred)
ypoints = np.array(latency_array_ms)
plt.xlabel('Total Bits Transferred')
plt.ylabel('Latency (milliseconds)')
plt.title('Latency vs Total Bits Transferred')
plt.plot(xpoints, ypoints)
plt.gca().get_xaxis().get_major_formatter().set_scientific(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.grid()
plt.show()

# Plot the Bandwidth vs Total Bits Transferred
xpoints = np.array(total_bits_transferred)
ypoints = np.array(bandwidth_array_bits_per_second)
plt.xlabel('Total Bits Transferred')
plt.ylabel('Bandwidth (Bits per Second)')
plt.title('Bandwidth vs Total Bits Transferred')
plt.plot(xpoints, ypoints)
plt.gca().get_xaxis().get_major_formatter().set_scientific(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.grid()
plt.show()

# Plot the Total Bits Transferred vs Elapsed Receive Time
xpoints = np.array(receive_time_array_ms)
ypoints = np.array(total_bits_transferred)
plt.ylabel('Total Bits Transferred')
plt.xlabel('Elapsed Receive Time (Milliseconds)')
plt.title('Total Bits Transferred vs Elapsed Receive Time')
plt.plot(xpoints-receive_time_array_ms[0], ypoints)
plt.gca().get_xaxis().get_major_formatter().set_scientific(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.grid()
plt.show()