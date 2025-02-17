#!/usr/bin/python3
# coding=utf8
import sys
import os
import cv2
import time
import queue
import logging
import threading
import RPCServer
import MjpgServer
import numpy as np

import hiwonder.Camera as Camera
import hiwonder.yaml_handle as yaml_handle

import Functions.Running as Running

# 主线程，已经以后台的形式开机自启
# 自启方式systemd，自启文件/etc/systemd/system/tonypi.service
# sudo systemctl stop tonypi  此次关闭
# sudo systemctl disable tonypi 永久关闭
# sudo systemctl enable tonypi 永久开启
# sudo systemctl start tonypi 此次开启

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

QUEUE_RPC = queue.Queue(10)

def startTonyPi():

    RPCServer.QUEUE = QUEUE_RPC

    threading.Thread(target=RPCServer.startRPCServer,
                     daemon=True).start()  # rpc服务器
    threading.Thread(target=MjpgServer.startMjpgServer,
                     daemon=True).start()  # mjpg流服务器
    
    loading_picture = cv2.imread('/home/pi/TonyPi/Functions/loading.jpg')
    cam = Camera.Camera()  # 相机读取
    
    open_once = yaml_handle.get_yaml_data('/boot/camera_setting.yaml')['open_once']
    if open_once:
        cam.camera_open()
    
    open_once
    Running.open_once = open_once
    Running.cam = cam

    while True:
        time.sleep(0.03)
        # 执行需要在本线程中执行的RPC命令
        while True:
            try:
                req, ret = QUEUE_RPC.get(False)
                event, params, *_ = ret
                ret[2] = req(params)  # 执行RPC命令
                event.set()
            except:
                break
        #####
        # 执行功能玩法程序：
        try:
            if Running.RunningFunc > 0 and Running.RunningFunc <= 9:
                if cam.frame is not None:
                    frame = cam.frame.copy()
                    img = Running.CurrentEXE().run(cam.frame)
                    if Running.RunningFunc == 9:
                        MjpgServer.img_show = np.vstack((img, frame))
                    else:
                        MjpgServer.img_show = img
                else:
                    MjpgServer.img_show = loading_picture
            else:
                if open_once:
                    MjpgServer.img_show = cam.frame
                else:
                    cam.frame = None
        except KeyboardInterrupt:
            break
        except BaseException as e:
            print('error', e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    startTonyPi()