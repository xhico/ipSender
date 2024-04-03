# -*- coding: utf-8 -*-
# !/usr/bin/python3


import os
import socket
import traceback
import datetime
import logging
import urllib.request
from picamera2 import Picamera2
from Misc import get911, sendEmail


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
    subject = localIp + " | " + externalIP + " | " + now
    body = subject.replace(" | ", "\n")

    # #  Take pic
    # IMG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMG_FILE.jpg")
    # with Picamera2() as camera:
    #     # Configure camera
    #     camera.configure(camera.create_still_configuration())
    #     # Start camera
    #     camera.start()
    #     # Capture image and save to file
    #     camera.capture_file(IMG_FILE)

    # Send email without image attachment
    sendEmail(subject, body)
    # sendEmail(subject, body, IMG_FILE)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace(".py", ".log")}")}"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
        sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        logger.info("End")
