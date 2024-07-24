import cv2
from subprocess import Popen, PIPE, STDOUT
import time
import threading
class Scrcpy(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.flag = True
    
    def poper(self):
        self.proc = Popen('scrcpy-win64-v2.5\scrcpy.exe', shell=True,stdout=PIPE)
    
    def run(self):
        while self.flag:
            self.poper()
            for line in iter(self.proc.stdout.readline, 'b'):
                if self.proc.poll() is not None:
                    if line == b'':
                        break
                    print(line.strip())
            print("restart")
            time.sleep(0.5)
    def stop(self):
        self.proc.kill()
if __name__ == '__main__':
    scrcpy = Scrcpy()
    scrcpy.start()
    try:
        while True:
            time.sleep(0.5)
    except:
        scrcpy.stop()
