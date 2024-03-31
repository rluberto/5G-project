# The client data file is responsible for processing the timestamp data that is sent from the client

import sys

# Read the data beign sent from the client
data = sys.stdin.read()

# Print the data
print("Received data:", data)