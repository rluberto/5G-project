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