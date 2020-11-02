import json

import time
import cv2
 
import subprocess
from subprocess import Popen, PIPE 

import requests
import json

from utils.util import video
from setting import logger
from utils.ap_check import wifi


if __name__=="__main__":
    wifi=wifi()


    url="http://192.168.4.1/SVGA"

    while True:
        if wifi.is_kana():

            print('KANA_CAM is in essid')
            wifi.connect_ap()

            url="http://192.168.4.1/SVGA"
            try:
                v = video(url)
                v.show(debug=True,send=False)

            except Exception as e:
                logger.info("Disconnect")
                logger.info("reaseon : " + e)
                subprocess.call(['sudo','nmcli','con','down','KANA_CAM'])
                subprocess.call(['sudo','nmcli','con','delete' ,'KANA_CAM'])
                cv2.destroyAllWindows()
                continue

        # else:
            # logger.info("No WiFi")