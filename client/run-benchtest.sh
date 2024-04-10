!/bin/bash

remote_server_ip=
remote_server_user=
remote_server_python_script=/home/rluberto/Lab/5G-project/server/server.py

local_client_transfer_file_path=media/video.mp4
local_client_python_script=/home/rock/5G-project/client/client.py

pid=$(ssh $remote_server_user@$remote_server_ip "nohup python3 $remote_server_python_script >

python3 $local_client_python_script $remote_server_ip $local_client_transfer_file_path
