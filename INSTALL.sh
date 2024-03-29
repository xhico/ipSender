#!/bin/bash

sudo mv /home/pi/ipSender/ipSender.service /etc/systemd/system/ && sudo systemctl daemon-reload
python3 -m pip install -r /home/pi/ipSender/requirements.txt --no-cache-dir
sudo apt install libatlas-base-dev libxslt-dev libcap-dev python3-libcamera python3-kms++ -y
chmod +x -R /home/pi/ipSender/*