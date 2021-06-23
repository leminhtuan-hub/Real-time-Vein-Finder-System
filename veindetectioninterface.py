# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter import messagebox
import threading
import datetime
import imutils
import cv2
import os
import PiVideoStream
import time
import argparse


# ap = argparse.ArgumentParser()
# ap.add_argument("-o", "--output", required=True, help="path to output directory to store snapshots")
# args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
ini = PiVideoStream.PiVideoStream()
vs = ini.start()
time.sleep(2.0)
proimg = -1

class VeinDetectionInterface:
    def __init__(self, vs):#, outputPath):
        self.vs = vs
        #self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("Vein Detection Device Software")
        self.panel = None
        self.image = None
        
        lab = tk.Label(self.root, text="Vein Finder Interface", fg ="blue", font = "Helvetica 16 bold")
        lab.pack()
        
        btnSnapshot = tk.Button(self.root, width=50, text="Snapshot", command=self.takeSnapshot)
        btnSnapshot.pack(side="bottom", padx=10, pady=10)
        
        btnProImg = tk.Button(self.root, width = 50, text="Processing", command= self.Processing)
        btnProImg.pack(side="bottom", padx=10, pady=10)

        sliderZoom = tk.Scale(self.root, from_=10, to=99, orient=tk.HORIZONTAL, label = "Zoom", command=self.Zoom)
        sliderZoom.set(99)
        sliderZoom.pack(side='right',padx=5, pady=5)

        sliderSharpness = tk.Scale(self.root, from_=-100, to=100, orient=tk.HORIZONTAL, label = "Sharpness", command=self.Sharpness)
        sliderSharpness.pack(side='right',padx=5, pady=5)

        sliderContrast = tk.Scale(self.root, from_=-100, to=100, orient=tk.HORIZONTAL, label = "Contrast", command=self.Contrast)
        sliderContrast.pack(side='right',padx=5, pady=5)

        sliderBrightness = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Brightness", command=self.Brightness)
        sliderBrightness.set(50)
        sliderBrightness.pack(side='right',padx=5, pady=5)

        self.stopEvent = threading.Event()
        #self.thread = threading.Thread(target=self.videoLoop, args=())
        #self.thread.start()
        self.videoLoop()
        

        self.root.wm_title("System Interface")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        
    def Brightness(self, value):
        global ini
        ini.camera.brightness = int(value)

    def Contrast(self, value):
        global ini
        ini.camera.contrast = int(value)

    def Sharpness(self, value):
        global ini
        ini.camera.sharpness = int(value)

    def Zoom(self, var):
        global ini
        x = float("0."+var)
        ini.camera.zoom = (0.1,0.1,x,x)
    
    def Processing(self):
        global proimg
        proimg = 2-(1-proimg)
         
    def videoLoop(self):
            global proimg
            if not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=545)
                if proimg == -1:
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                elif proimg == 0:
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    self.frame = cv2.medianBlur(self.frame,3)
                elif proimg == 1:
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    self.frame = cv2.medianBlur(self.frame,3)
                    self.frame = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(self.frame)
                    self.frame = cv2.GaussianBlur(self.frame,(5,5),0)
                    self.frame = cv2.medianBlur(self.frame,5)
                    #self.frame = cv2.adaptiveThreshold(self.frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
                else:
                    proimg = -1
 
                image = Image.fromarray(self.frame)
                image = ImageTk.PhotoImage(image)
                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
            self.panel.after(10, self.videoLoop)                    
        
    def takeSnapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join(('/home/pi/Desktop/output', filename))
        
        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))
        messagebox.showinfo('Save Images', 'Sucessfully Saved Image')
    
    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

# start the app
vein = VeinDetectionInterface(vs)#, args["output"])
vein.root.mainloop()

