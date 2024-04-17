#!/bin/bash

remote_server_ip=[ip address]
remote_server_user=[username]

remote_server_python_script=/home/[username]/5G-project/server/server.py
remote_server_output_file_path=/home/[username]/5G-project/server/media
local_client_transfer_file_path=/home/[username]/5G-project/client/media/image.jpg
local_client_python_script=/home/[username]/5G-project/client/client.py


TS=$(date +%s)
benchmark_name="_benchmark.json"
out_file="${TS}${benchmark_name}"

ssh $remote_server_user@$remote_server_ip "nohup python3 $remote_server_python_script $remote_server_ip $TS > /home/[username]/server_out.txt 2>%1 &"
sleep 1

python3 $local_client_python_script $remote_server_ip $local_client_transfer_file_path

cd /home/rock/benchmark_output
scp [username]@$remote_server_ip:/home/[username]/5G-project/server/benchmark-data/$out_file ./