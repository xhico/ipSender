# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install requests yagmail picamera2 numpy lxml --no-cache-dir
# sudo apt install libatlas-base-dev libxslt-dev -y

import os
import socket
import traceback
import datetime
import logging
import urllib.request
import yagmail
from picamera2 import Picamera2
from Misc import get911


def main():
    """
    This script gets the hostname, local IP address, external IP address, and sends an email
    with this information. If the hostname is "RPI4", it also takes a picture and attaches it to the email.

    Dependencies:
        - socket
        - urllib
        - datetime
        - os (if hostname == "RPI4")
        - picamera (if hostname == "RPI4")
        - yagmail

    Usage:
        - Modify the EMAIL_USER, EMAIL_APPPW, and EMAIL_RECEIVER variables with appropriate values.
        - Run the script.

    Returns:
        None.
    """
    
    # Get hostname
    hostname = socket.gethostname()
    logger.info(hostname)

    # Get localIp
    localIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localIp.connect(("8.8.8.8", 80))
    localIp = localIp.getsockname()[0]
    logger.info(localIp)

    # Get externalIP
    externalIP = urllib.request.urlopen("https://v4.ident.me/").read().decode("utf8")
    logger.info(externalIP)

    # Send email
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    subject = hostname + " | " + localIp + " | " + externalIP + " | " + now
    body = subject.replace(" | ", "\n")

    #  Take pic
    if hostname == "RPI4":
        IMG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMG_FILE.jpg")
        with Picamera2() as camera:
            # Configure camera
            camera.configure(camera.create_still_configuration())
            # Start camera
            camera.start()
            # Capture image and save to file
            camera.capture_file(IMG_FILE)
        # Send email with image attachment
        yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, subject, body, IMG_FILE)
    else:
        # Send email without image attachment
        yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, subject, body)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath(__file__).replace(".py", ".log"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    EMAIL_USER = get911('EMAIL_USER')
    EMAIL_APPPW = get911('EMAIL_APPPW')
    EMAIL_RECEIVER = get911('EMAIL_RECEIVER')

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
    finally:
        logger.info("End")
