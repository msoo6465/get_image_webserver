import json

import time
import cv2
 
import subprocess
from subprocess import Popen, PIPE

import requests
import json

from utils.util import video
from setting import logger


if __name__=="__main__":
    sudo_password = 'nano'
    command = ['sudo','nmcli','con']
    p = Popen(['sudo','-S']+command,stdin=PIPE,stderr=PIPE,universal_newlines=True)
    sudo_pormpt = p.communicate('nano'+'\n')[1]
    a = subprocess.check_output(['sudo','nmcli','con'])

    #change to your ESP32-CAM ip
    url="http://192.168.4.1/SVGA"
    # CAMERA_BUFFRER_SIZE=4096
    while True:
        wifi_list = subprocess.check_output(['sudo','nmcli','d','wifi','list'])
        wifi_list = str(wifi_list)
        essid = []

        wifi_list = wifi_list.split(' ')
        for index ,wifi in enumerate(wifi_list):
            if wifi == ' ' or wifi == '' or wifi == '\\n':
                continue
            else:
                essid.append(wifi)

        # print(essid)
        if 'KANA_CAM' in essid:
            print('KANA_CAM is in essid')
            subprocess.call(['sudo','nmcli','d','wifi','con','KANA_CAM','password','1q2w3e4r'])
            url="http://192.168.4.1/SVGA"

            v = video(url)
            v.show(save=True)
            print('1')
            # try:
                # v.show(save=True)
                # print('1')
            # except Exception as e:
            #     print(e)
            #     continue
        else:
            logger.info("No WiFi")