import subprocess
from subprocess import Popen, PIPE 



class wifi():
    def __init__(self):
        self.sudo_password = 'nano'
        command = ['sudo','nmcli','con']
        p = Popen(['sudo','-S']+command,stdin=PIPE,stderr=PIPE,universal_newlines=True)
        sudo_pormpt = p.communicate('nano'+'\n')[1]
        a = subprocess.check_output(['sudo','nmcli','con'])

    def is_kana(self):

        wifi_list = subprocess.check_output(['sudo','nmcli','d','wifi','list'])
        wifi_list = str(wifi_list)
        essid = []

        wifi_list = wifi_list.split(' ')
        for index ,wifi in enumerate(wifi_list):
            if wifi == ' ' or wifi == '' or wifi == '\\n':
                continue
            else:
                essid.append(wifi)

        if 'KANA_CAM' in essid:
            return True
        else:
            return False

    def connect_ap(self):
        subprocess.call(['sudo','nmcli','d','wifi','con','KANA_CAM','password','1q2w3e4r'])