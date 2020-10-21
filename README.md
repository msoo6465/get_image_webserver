# get_image_webserver README
## Change CUI cammand
To disable GUI on boot, run:

    sudo systemctl set-default multi-user.target
   
To enable GUI again issue the command:

    sudo systemctl set-default graphical.target
    
to start Gui session on a system without a current GUI just execute:

    sudo systemctl start gdm3.service
    
    
## Jetson nano install pytorch
if jetpack version >= 4.2
pytorch == 1.6.0
torchvision == 0.7.0

    wget https://nvidia.box.com/shared/static/9eptse6jyly1ggt9axbja2yrmj6pbarc.whl -O torch-1.6.0-cp36-cp36m-linux_aarch64.whl 
    sudo apt-get install python3-pip libopenblas-base libopenmpi-dev
    pip3 install Cython
    pip3 install numpy torch-1.6.0-cp36-cp36m-linux_aarch64.whl
    
torchvision

    sudo apt-get install libjpeg-dev zlib1g-dev
    git clone --branch <version> https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
    cd torchvision
    export BUILD_VERSION=0.x.0  # where 0.x.0 is the torchvision version  
    sudo python setup.py install     # use python3 if installing for Python 3.6
    cd ../  # attempting to load torchvision from build dir will result in import error
    pip install 'pillow<7' # always needed for Python 2.7, not needed torchvision v0.5.0+ with Python 3.6
    
    PyTorch v1.0 - torchvision v0.2.2
PyTorch v1.1 - torchvision v0.3.0
PyTorch v1.2 - torchvision v0.4.0
PyTorch v1.3 - torchvision v0.4.2
PyTorch v1.4 - torchvision v0.5.0
PyTorch v1.5 - torchvision v0.6.0
PyTorch v1.6 - torchvision v0.7.0


## install nano
    sudo apt-get install supervisor
    
    sudo gedit /etc/supervisor/conf.d/kana.conf
    ====add to kana.conf=====
    [program:kana]
    command=command=/usr/bin/python3 /home/nano/lib/get_image_webserver/main.py
    directory=/home/nano/lib/get_image_webserver
    autostart=yes
    autorestart=yes
    startsecs=5
    startretries=3
    sterr_logfile=/home/nano/lib/get_image_webserver/logs/kana.err.log
    user=nano
    =========================
    
    ====supervisor command=====
    sudo supervisord
    sudo supervisorctl update
    sudo supervisorctl reread
    sudo supervisorctl reload
    sudo supervisorctl start kana
    sudo supervisorctl status


## main.py

    python3 main.py