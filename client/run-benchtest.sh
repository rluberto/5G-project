#!/bin/bash

remote_server_ip=
remote_server_user=
remote_server_python_script=Developer/5G-project/server/server.py

local_client_transfer_file_path=media/video.mp4
local_client_python_script=client/client.py

read -s -p "Enter SSH password: " ssh_password

sshpass -p "$ssh_password" ssh $remote_server_user@$remote_server_ip "python3 $remote_python_script $remote_server_ip $local_client_transfer_file_path"

python3 $local_client_python_script "$remote_server_ip $local_client_transfer_file_path"