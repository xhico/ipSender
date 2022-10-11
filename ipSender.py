# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install requests yagmail picamera numpy lxml --no-cache-dir
# sudo apt install libatlas-base-dev libxslt-dev -y

import json
import os
import socket
import traceback
import datetime
import logging
import requests
import yagmail
import base64
from picamera2 import Picamera2
from Misc import get911


def main():
    # Get hostname
    hostname = socket.gethostname()
    logger.info(hostname)

    # Get localIp
    localIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localIp.connect(("8.8.8.8", 80))
    localIp = localIp.getsockname()[0]
    logger.info(localIp)

    # Get externalIp
    externalIp = requests.get('https://api.ipify.org').content.decode('utf8')
    logger.info(externalIp)

    # Take pic
    with Picamera2() as camera:
        camera.start()
        camera.capture_file(IMG_FILE)

    # Send email
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    subject = hostname + " | " + localIp + " | " + externalIp + " | " + now
    body = subject.replace(" | ", "\n")
    yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, subject, body, IMG_FILE)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath(__file__).replace(".py", ".log"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    EMAIL_USER = get911('EMAIL_USER')
    EMAIL_APPPW = get911('EMAIL_APPPW')
    EMAIL_RECEIVER = get911('EMAIL_RECEIVER')
    IMG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMG_FILE.jpg")

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
    finally:
        logger.info("End")
