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
        self.stream=urlopen(url,timeout = 10.0)
        self.reset=True

        self.kana_type = {'fall_down':'어르신의 "중심을 잃고 쓰러짐"이(가) 감지되었습니다.' ,
                            'stumble':'어르신의 "비틀거림"이(가) 감지되었습니다.',
                            'motionless':'어르신의 "움직임"이(가) 감지되지 않습니다.',
                            'seizure':'어르신의 "발작,간질"이(가) 감지되었습니다.',
                            'reset_test':'초기 카메라 테스트''}

        self.feline_type = {'stand':'문 앞에 서있는 사람 감지',
                            'touch_doorlock':'도어락 조작 감지',
                            'peep':'외서경에 눈을 대는 행위 감지',
                            'eavesdrop':'문에 귀를 대는 행위 감지',
                            'touch_bell':'초인종 조작 행위 감지',
                            'knock':'노크 행위 감지',
                            'put_object':'물건 놓는 행위 감지',
                            'take_object':'절도 의심 행위 감지',
                            'use_device':'전자기기 조작행위 감지',
                            'stick_leaflet':'전단지 부착 행위 감지',
                            'hold_weapon':'무기 소지자 감지',
                            'reset_test':'초기 카메라 테스트'}

        self.tot_time = 0
        self.count = 0

    def send_server(self,image,mode,gkey,reset):
        url = 'http://121.151.110.163:9001/'
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjEsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsIndobyI6Im1lbWJlciIsImlhdCI6MTYwMDI0NDIwNywiZXhwIjoxNjMxNzgwMjA3LCJpc3MiOiJrYW5hZmVsaW5lLmNvLmtyIiwic3ViIjoidXNlcmluZm8ifQ.DAOURYXRfQBy5dCGwqWhQwD7DFxlK1_wP6LKYEQJ4e8'
        headers = { 'i-access-token': 'kanaiamdsilfamadsjfoge', 'x-access-token': token}
        

        _, img_encoded = cv2.imencode('.jpg', image)

        files = [('detectedImages', ('img', img_encoded.tostring(), 'image/jpeg'))]
        if mode == 'feline':
            print(url+'upload')
            data = {'serial': 'test-serial-2', 'type': self.feline_type[int(random.choice(string.digits)+random.choice(string.digits))%len(self.feline_type)], 'contents': 'This is for test', 'gkey': str(gkey)}
            if reset:
                data['type']='reset_test'
                data['contents']=self.feline_type['reset_test']
            print(data)
            # res = requests.post(url+'upload',data=data,headers=headers,files=files)

        elif mode == 'kana':
            print(url+'camlog/log')
            # data = {'serial': 'C3WQ0VGUTE', 'type': self.kana_type[int(random.choice(string.digits)+random.choice(string.digits))%len(self.kana_type)], 'contents': 'This is for test', 'gkey':str(gkey)}
            data = {'serial': 'C3WQ0VGUTE', 'type': 'motionless', 'contents': self.kana_type['motionless'], 'gkey':str(gkey)}
            if reset:
                data['type']='reset_test'
                data['contents']=self.feline_type['reset_test']
            print(data)
            # res = requests.post(url+'camlog/log',data=data,headers=headers)
        
        # print(res.status_code)

    def show(self,save= False,debug = False,send=True):
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
                        gkey = ''
                        for i in range(_LENGTH):
                            self.reset = False
                            gkey += random.choice(string.ascii_letters)

                    start_time = time.time()
                    if send:
                        self.send_server(img,mode='kana',gkey=gkey,reset=self.reset)

            k=cv2.waitKey(1)
            if k & 0xFF==ord('q'):
                logger.info(self.tot_time/self.count)
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
