#!/bin/bash

remote_server_ip=
remote_server_user=
remote_server_python_script=Lab/5G-project/server/server.py

local_client_transfer_file_path=media/video.mp4
local_client_python_script=client/client.py

pid=S(ssh $remote_server_user@$remote_server_ip "nohup python3 $remote_server_python_script $remote_server_ip > /dev/null 2>&1 & echo \S!")

python3 $local_client_python_script "$remote_server_ip $local_client_transfer_file_path"