import matplotlib.pyplot as plt
import numpy as np
import json

data_file_path = 'benchmark-data/269607_benchmark.json'
data = json.load(open(data_file_path))

sent_time_array = data['sent_time_array']
receive_time_array = data['receive_time_array']
latency_array = data['latency_array']

xpoints = np.array(sent_time_array)
ypoints = np.array(latency_array)

plt.plot(ypoints)
plt.show()