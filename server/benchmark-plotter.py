import matplotlib.pyplot as plt
import numpy as np
import json

# Change the number below to select the json file you want to plot
benchmark_file_number = 576069

data_file_path = 'benchmark-data/'+str(benchmark_file_number)+'_benchmark.json'
data = json.load(open(data_file_path))

sent_time_array = data['sent_time_array']
receive_time_array = data['receive_time_array']
latency_array = data['latency_array']

xpoints = np.array(sent_time_array)
ypoints = np.array(latency_array)

plt.plot(ypoints)
plt.show()