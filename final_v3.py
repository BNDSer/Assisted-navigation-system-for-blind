# encodin: utf-8

import threading
import cv2
from ultralytics import YOLO
import time
import winsound
import numpy
import torch
import pyttsx3

class RTSCapture(cv2.VideoCapture):
    """Real Time Streaming Capture.
    这个类必须使用 RTSCapture.create 方法创建，请不要直接实例化
    """

    _cur_frame = None
    _reading = False
    schemes = ["rtsp://", "rtmp://"] #用于识别实时流

    @staticmethod
    def create(url, *schemes):
        """实例化&初始化
        rtscap = RTSCapture.create("rtsp://example.com/live/1")
        or
        rtscap = RTSCapture.create("http://example.com/live/1.m3u8", "http://")
        """
        rtscap = RTSCapture(url)
        rtscap.frame_receiver = threading.Thread(target=rtscap.recv_frame, daemon=True)
        rtscap.schemes.extend(schemes)
        if isinstance(url, str) and url.startswith(tuple(rtscap.schemes)):
            rtscap._reading = True
        elif isinstance(url, int):
            # 这里可能是本机设备
            rtscap._reading = True

        return rtscap

    def isStarted(self):
        """替代 VideoCapture.isOpened() """
        ok = self.isOpened()
        if ok and self._reading:
            ok = self.frame_receiver.is_alive()
        return ok

    def recv_frame(self):
        """子线程读取最新视频帧方法"""
        while self._reading and self.isOpened():
            ok, frame = self.read()
            if not ok: break
            self._cur_frame = frame
        self._reading = False

    def read2(self):
        """读取最新视频帧
        返回结果格式与 VideoCapture.read() 一样
        """
        frame = self._cur_frame
        self._cur_frame = None
        return frame is not None, frame

    def start_read(self):
        """启动子线程读取视频帧"""
        self.frame_receiver.start()
        self.read_latest_frame = self.read2 if self._reading else self.read

    def stop_read(self):
        """退出子线程方法"""
        self._reading = False
        if self.frame_receiver.is_alive(): self.frame_receiver.join()

model = YOLO('D:/ZichenFeng/Python/runs/detect/train34/weights/best.pt')
#model = YOLO('yolov8n.pt')
#model = YOLO('yolov8n-pose.pt')
#model = YOLO('yolov8n-seg.pt')


rtscap = RTSCapture.create(2)
#rtscap = RTSCapture.create('D:/ZichenFeng/Python/deeplearning/guider/test_vid/VID1.mp4')
#rtscap = RTSCapture.create("rtsp://admin:admin@192.168.43.1:8554/live")
#rtscap = RTSCapture.create("rtsp://admin:admin@10.5.4.253:8554/live")


'''names: {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}'''


rtscap.start_read() #启动子线程并改变 read_latest_frame 的指向


# boxes = None
boxes = torch.tensor([])
boxes.cls = torch.tensor([])

tim = 0
frequency = 0
under = -1
center = -2
a = -2
read_list = []


def check_distant():
    global under
    global tim
    global frequency
    while True:

        if under == -1:
            tim = 0
            frequency = 0
            time.sleep(0.1)
        elif under <= 1 and under >= 0.75:
            tim = 100+(1-under)*(400/0.25)
            tim = int(tim)
            frequency = 1800+(under-0.75)*(400/0.25)
            frequency = int(frequency)
            print(under)
            time.sleep(0.1)
        else:
            tim = 0
            frequency = 0
            time.sleep(0.1)

threading.Thread(target=check_distant, args = ()).start()


def beep():
    global tim 
    global frequency
    while True:
        if tim > 0 and frequency > 0:
            #winsound.Beep(2000, m)
            winsound.Beep(frequency, tim)
            t = ((tim*0.6)/1000)
            time.sleep(t)
        else:
            time.sleep(0.1)

threading.Thread(target=beep, args = ()).start()





def check_broad():
    global read_list
    global a
    global i
    global center

    time.sleep(3)

    if len(Broad_list) > 0:
        #pyttsx3.speak('Spotted broad')
        read_list.append('Spotted broad')
    else:
        read_list.append('No broad found')


    while True:
        if len(Broad_list) > 0:
            if center >= 0.65 or center <= 0.35:
                # i = 1
                # print('not on broad')
                if center <= 0.35:
                    i = 1
                    # print('right')
                if center >= 0.65:
                    i = 2
                    # print('left')
            else:
                i = 0
                # print('on broad')
        else:
            i = -1
            # pyttsx3.speak('No broad found')



        if i == -1 and a != i:
            # pyttsx3.speak('No broad found')
            read_list.append('No broad found')
            a = i
            #time.sleep(2)
        if i == 0 and a != i:
            # pyttsx3.speak('on broad')
            read_list.append('on broad')
            a = i
            #time.sleep(2)

        if i == 1 or i == 2:
            if i == 1:
                # pyttsx3.speak('right')
                read_list.append('turn left')
                a = i
                #time.sleep(5)
            elif i == 2:
                # pyttsx3.speak('left')
                read_list.append('turn right')
                a = i
                #time.sleep(5)
                
        time.sleep(2.5)


threading.Thread(target=check_broad, args = ()).start()



def read_part():
    global read_list
    while True:
        if len(read_list) > 0:
            pyttsx3.speak(read_list[0])

            if len(read_list) > 0 : # 解决read_list与check_box同时修改list问题
                del read_list[0]
        else:
            time.sleep(0.3)


threading.Thread(target=read_part, args = ()).start()



nearestObjectList = list()
confFitlist = list()
position_Fitlist  = list()
Broad_list = list()

 
while rtscap.isStarted():
    ok, frame = rtscap.read_latest_frame() #read_latest_frame() 替代 read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if not ok:
        continue

    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Inference", annotated_frame)

    # get the results
    boxes = results[0].boxes
    boxes.cls
    boxes = boxes.cpu()
    boxes = boxes.numpy()
    # print(boxes.xyxyn)


    confFitlist.clear()
    for obj in boxes:
        if obj.conf[0] >= 0.3:
            confFitlist.append(obj)

    Broad_list.clear()
    center = -1     #
    for obj in confFitlist:
        if obj.cls == 1:
            Broad_list.append(obj)
            center = (obj.xyxyn[0][2]+obj.xyxyn[0][0])*0.5
            break
            


    position_Fitlist.clear()
    for obj in confFitlist:
        if obj.xyxyn[0][2] > 0.4 and obj.xyxyn[0][0] < 0.6:
            position_Fitlist.append(obj)

    nearestObjectList.clear()
    under = -1
    for obj in position_Fitlist:
        if obj.cls !=0 and obj.cls !=2 and obj.cls !=3:
            continue

        index = -1
        for num in range(len(nearestObjectList)):
            if nearestObjectList[num].cls == obj.cls:
                index = num
                break
        if index > -1:
            nearestObject = nearestObjectList[index]
            if obj.xyxyn[0][3] > nearestObject.xyxyn[0][3]:
                nearestObjectList[index] = obj
        else:
            nearestObjectList.append(obj)

    for nearestObject in nearestObjectList:
        # print('nearestObject='+str(nearestObject))
        under = nearestObject.xyxyn[0][3]

    
rtscap.stop_read()
rtscap.release()
cv2.destroyAllWindows()
