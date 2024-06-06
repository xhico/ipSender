# -*- coding: utf-8 -*-
# !/usr/bin/python3


import Misc
import datetime
import logging
import os
import socket
import traceback
import urllib.request


def main():
    """
    This script gets the hostname, local IP address, external IP address, and sends an email
    with this information.

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

    # Send email
    Misc.sendEmail(subject, body)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace('.py', '.log')}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
        Misc.sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        logger.info("End")
