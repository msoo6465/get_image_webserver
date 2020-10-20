import time

import cv2
import numpy as np
from urllib.request import urlopen
 
import sys
import select
import subprocess
from subprocess import Popen, PIPE

import requests
import json
import random
import string
import os

from setting import logger


class video():
    def _isData(self):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    
    def __init__(self,url):
        self.url = url
        self.stream=urlopen(url,timeout = 2.0)

        self.kana_type = ['fall_down','stumble','motionless','seizure']
        self.feline_type = ['stand','touch_doorlock','peep','eavesdrop','youch_bell','knock','look_around','put_object','take_object','take_object','use_device','stick_leaflet','hold_weapon']
        self.tot_time = 0
        self.count = 0

    def send_server(self,image,mode,gkey):
        url = 'http://121.151.110.163:9001/'
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjEsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsIndobyI6Im1lbWJlciIsImlhdCI6MTYwMDI0NDIwNywiZXhwIjoxNjMxNzgwMjA3LCJpc3MiOiJrYW5hZmVsaW5lLmNvLmtyIiwic3ViIjoidXNlcmluZm8ifQ.DAOURYXRfQBy5dCGwqWhQwD7DFxlK1_wP6LKYEQJ4e8'
        headers = { 'i-access-token': 'kanaiamdsilfamadsjfoge', 'x-access-token': token}
        

        _, img_encoded = cv2.imencode('.jpg', image)

        files = [('detectedImages', ('img', img_encoded.tostring(), 'image/jpeg'))]
        if mode == 'feline':
            print(url+'upload')
            data = {'serial': 'test-serial-2', 'type': self.feline_type[int(random.choice(string.digits)+random.choice(string.digits))%len(self.feline_type)], 'contents': 'This is for test', 'gkey': str(gkey)}
            print(data)
            # res = requests.post(url+'upload',data=data,headers=headers,files=files)

        elif mode == 'kana':
            print(url+'camlog/log')
            data = {'serial': 'test-serial-2', 'type': self.kana_type[int(random.choice(string.digits)+random.choice(string.digits))%len(self.kana_type)], 'contents': 'This is for test', 'gkey':str(gkey)}
            print(data)
            res = requests.post(url+'camlog/log',data=data,headers=headers)
        
        print(res.status_code)

    def show(self,save= False,debug = False):
        bts=b''
        imgs = []
        start_time = time.time()
        sample_time = time.time()
        _LENGTH = 15
        gkey = ''

        for i in range(_LENGTH):
            gkey += random.choice(string.ascii_letters)

        while True:
            bts+=self.stream.read(4096)
            jpghead=bts.find(b'\xff\xd8')
            jpgend=bts.find(b'\xff\xd9')
            if self._isData():
                c = list(map(str,sys.stdin.readline().split()))
                self.change(c)
                self.tot_time = 0
                self.count = 0
                bts = b''
                print(1)
                continue

            if jpghead>-1 and jpgend>-1:
                jpg=bts[jpghead:jpgend+2]
                bts=bts[jpgend+2:]

                try:
                    img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
                except Exception as e:
                    logger.info(e)
                    continue

                v=cv2.flip(img,0)
                h=cv2.flip(img,1)
                p=cv2.flip(img,-1)
                frame=p
                h,w=frame.shape[:2]
                
                if self.count<5:
                    print(frame.shape)
                    print(w,h)
                    
                img=cv2.resize(frame,(w,h))

                if debug:
                    cv2.imshow("a",img)

                end_time = time.time()
                a = end_time-start_time
                self.tot_time += end_time-start_time
                if save:
                    if not os.path.isdir('./imgs'):
                        os.mkdir('./imgs')
                    cv2.imwrite(f'./imgs/img_{self.count}.png',img)

                self.count+=1
                

                if time.time() - start_time > 3:
                    if time.time()-sample_time > 20:
                        sample_time = time.time()
                        
                        for i in range(_LENGTH):
                            gkey += random.choice(string.ascii_letters)

                    start_time = time.time()
                    print(gkey)
                    self.send_server(img,mode='kana',gkey=gkey)

            k=cv2.waitKey(1)
            if k & 0xFF==ord('q'):
                print(self.tot_time/self.count)
                subprocess.call(['sudo','nmcli','con','down','KANA_CAM'])
                subprocess.call(['sudo','nmcli','con','delete' ,'KANA_CAM'])
                exit()

    
    def change(self,url):
        cv2.destroyAllWindows()
        print('input data : ',url)
        if url == []:
            new_url = self.url
        else:
            new_url = self.url+url[0]
        del self.stream

        try:
            self.stream = urlopen(new_url,timeout=5)
            if url[0]=='dis':
                subprocess.call(['sudo','nmcli','con','down','KANA_CAM'])
                return
        except Exception as e:
            if url[0]=='dis':
                subprocess.call(['sudo','nmcli','con','down','KANA_CAM'])
                return
            print(e)
        print(self.stream)
        time.sleep(2)
