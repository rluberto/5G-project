import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Use command line arguement to get benchmark file number
benchmark_file_number = sys.argv[1]

data_file_path = 'benchmark-data/'+str(benchmark_file_number)+'_benchmark.json'
data = json.load(open(data_file_path))

sent_time_array = data['sent_time_array']
receive_time_array = data['receive_time_array']
latency_array = data['latency_array']
bandwidth_array = data['bandwidth_array']
transferred_data_length_array = data['transferred_data_length_array']

xpoints = np.array(sent_time_array)
ypoints = np.array(latency_array)

plt.xlabel('Bytes Sent (x 2048)')
plt.ylabel('Latency (Milliseconds)')
plt.title('Latency vs Bytes Sent')
plt.plot(ypoints*1000)
plt.show()

xpoints = np.array(sent_time_array)
ypoints = np.array(bandwidth_array)

plt.xlabel('Bytes Sent (x 2048)')
plt.ylabel('Bandwidth (Bits/Second)')
plt.title('Bandwidth vs Bytes Sent')
plt.plot(ypoints*8)
plt.show()

total_bytes_transferred_array = []
for i in range(len(transferred_data_length_array)):
    total_bytes_transferred_array.append(sum(transferred_data_length_array[:i+1]))

xpoints = np.array(receive_time_array)
ypoints = np.array(total_bytes_transferred_array)

plt.ylabel('Total Bytes Transferred')
plt.xlabel('Receive Time (Milliseconds)')
plt.title('Total Bytes Transferred vs Receive Time')
plt.plot((xpoints-receive_time_array[0])*1000, ypoints, marker='o')
plt.show()