#!/bin/bash

sudo mv /home/pi/ipSender/ipSender.service /etc/systemd/system/ && sudo systemctl daemon-reload
python3 -m pip install requests yagmail picamera2 numpy lxml --no-cache-dir
sudo apt install libatlas-base-dev libxslt-dev libcap-dev python3-libcamera -y
chmod +x -R /home/pi/ipSender/*