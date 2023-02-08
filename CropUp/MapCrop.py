#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 01:02:46 2022

@author: pascalyamlome
"""
import nrrd as nd
import cv2
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.constants import *
from PIL import Image, ImageTk
import cv2
import numpy as np
#import ImageViewer
from ImageViewer import ImageViewer
import matplotlib.pyplot as plt


class MapCrop():
    def __init__(self, win):
        
        self.currfilename = ''
        self.originalImg = None
        self.frame_cordinate = (None,None)
        self.frame_cordinate = (None,None)
        
        
        self.btn_path = Button(win, text='...', command=self.select_file)
        self.btn_path.place(x=10, y=3)
        
        #get defalt btn collor
        self.origbtn_color = self.btn_path.cget("background")
        
        self.txt_path = Entry()
        self.txt_path.place(x=40,y=5, width=770)
        
        self.btn_loadImg = Button(win, text='Load Img', command=self.load_image)
        self.btn_loadImg.place(x=840, y = 4, width = 135)
        
        self.lbl1=Label(win, text='The State buttons below\nRed = Active  \nGray = inactive')
        self.lbl1.place(x=840, y=40)
        
        self.btn_ImageArea = Button(win, text='Draw Image Area', command =self.ImageAreaSelectTask)
        self.btn_ImageArea.place(x=840, y = 100, width = 100)
        
        self.btn_ImgAreClc = Button(win, text='clc', command= self.btn_ImgAreClcTask)
        self.btn_ImgAreClc.place(x=945, y = 100, width = 30)
        
        
        
        self.btn_ROIArea = Button(win, text='Draw ROI Area', command = self.ROIAreaSelectTask)
        self.btn_ROIArea.place(x=840, y = 140, width = 100)
        
        self.btn_ROIAreaClc = Button(win, text='clc', command = self.btn_ROIAreClcTask)
        self.btn_ROIAreaClc.place(x=945, y = 140, width = 30) 
        
        
        self.btn_clearall = Button(win, text='Clear All', command =self.btn_ClearAllTask)
        self.btn_clearall.place(x=840, y = 180, width = 135)
        
        
        self.btn_Cropout = Button(win, text=' Crop out Image', command = self.cropImg)
        self.btn_Cropout.place(x=840, y = 220, width = 135)
        
        
        self.image_viewer = ImageViewer(master=win, w = 800, h = 700)
        self.image_viewer.place(x = 10, y= 40)
        #self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)
        #self.canvas = tk.Canvas(win, bg='gray', width=800,height=400)
        #self.canvas.place(relx = 0.1, rely= 0.1)
        
        
        self.slider = Scale(win, from_=500, to=2000, orient=HORIZONTAL, command = self.updateimg)
        self.slider.place(x=838, y = 280,width = 140)
        
        
        
    def cropImg(self):
        d1 = self.image_viewer.imcrop[2][0]
        d2 = self.image_viewer.imcrop[2][1]
        
        x1 = self.image_viewer.imcrop[0][0] 
        x2 = self.image_viewer.imcrop[1][0] 
        
        y1 = self.image_viewer.imcrop[0][1] 
        y2 = self.image_viewer.imcrop[1][1]
        
        print(self.image_viewer.imcrop)
        print(x1,y1, x2,y2, d1,d2)
        
        CroppedImg = self.originalImg[y1:y1+d1, x1:x1+d1]
        print(CroppedImg.shape)
        print(CroppedImg)
        
        relX = x2-x1
        rely = y2-y1
        dim = d2
        imgplot = plt.imshow(CroppedImg)
        
        

    def updateimg(self):
        self.C = self.slider.get()
        #self.image_viewer.show_image(self.originalImg, self.C)
        
    def ImageAreaSelectTask(self):
        self.btn_ImageArea.config(bg='red')
        self.image_viewer.activate_Areadraw()
        #print("we want to draw")
        
    def btn_ImgAreClcTask(self):
        self.btn_ImageArea.config(bg=self.origbtn_color)
        self.image_viewer.deactivate_draw()

    def ROIAreaSelectTask(self):
        self.btn_ROIArea.config(bg='green')
        self.image_viewer.activate_ROIdraw()
        #print("we want to draw")
        
    def btn_ROIAreClcTask(self):
        self.btn_ROIArea.config(bg=self.origbtn_color)
        
    def btn_ClearAllTask(self):
        self.image_viewer.clear_draw()
        self.image_viewer.deactivate_draw()
        self.btn_ROIArea.config(bg=self.origbtn_color)
        self.btn_ImageArea.config(bg=self.origbtn_color)
        self.image_viewer.show_image(self.originalImg)
        #print(win.imcrop)
        
        
        
        
        
        
        #ImageViewer.activate_draw()
        
    
    def select_file(self):
        #set the file types to be read
        '*.jpg;*.tif;*.png;*.gif; *.nrrd; *.DCM'
        filetypes = (('nrrd file', '*.nrrd'),
                     ('jpg img', '*.csv'),
                     ('tif img','*.tif'),
                     ('PNG img','*.png'),
                     ('DCM file', '*.DCM'),
                     ('All files', '*.*'))
        #obtain filename and parse it to the text box
        filename = fd.askopenfilename(
            title='Open a file',initialdir='/', filetypes=filetypes)
        
        self.currfilename = filename 
        self.txt_path.insert(END, str(filename))
    
    def load_image(self):
        path = self.currfilename
        file  = nd.read(path)
        #print(file[1])
        self.C = self.slider.get()

        imagedata = np.array(file[0])
        image = (imagedata[:,:])
        
        self.originalImg  = image.copy()
        img_scaled = image
        #img_scaled = cv2.normalize(image, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
        self.image_viewer.show_image(img_scaled, self.C)


    
        # self.lbl1=Label(win, text='First number')
        # self.lbl2=Label(win, text='Second number')
        # self.lbl3=Label(win, text='Result')
        # self.t1=Entry(bd=3)
        # self.t2=Entry()
        # self.t3=Entry()
        # self.btn1 = Button(win, text='Add')
        # self.btn2=Button(win, text='Subtract')
        # self.lbl1.place(x=100, y=50)
        # self.t1.place(x=200, y=50)
        # self.lbl2.place(x=100, y=100)
        # self.t2.place(x=200, y=100)
        # self.b1=Button(win, text='Add', command=self.add)
        # self.b2=Button(win, text='Subtract')
        # self.b2.bind('<Button-1>', self.sub)
        # self.b1.place(x=100, y=150)
        # self.b2.place(x=200, y=150)
        # self.lbl3.place(x=100, y=200)
        # self.t3.place(x=200, y=200)
        
        
        
        
window=Tk()
mywin=MapCrop(window)
window.title('MapCrop')
window.geometry("1000x800+10+10")
window.mainloop()

