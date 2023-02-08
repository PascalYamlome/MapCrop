

from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageViewer(Frame):

    def __init__(self, master=None, w = 600, h = 400):
        Frame.__init__(self, master=master, bg="black", width=w, height=h)
        self.imcrop = [[0,0],[0,0], [0,0]]
        self.shown_image = None
        self.x = 0
        self.y = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.draw_ids = list()
        self.rectangle_id = 0
        self.ratio = 0
        self.scale = 1

        self.canvas = Canvas(self, bg="black", width=w, height=h)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    def normalize(self,arr,c=1500, w = 800, n=1):
        """
        Linear normalization
        http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
        """
        arr = arr.astype('float')
        # Do not touch the alpha channel
        for i in range(n):
            #minval = arr[...,i].min()
            #maxval = arr[...,i].max()
            #mval = np.mean(arr)
            Omin = c-w
            Omax = c+w
            Nmin = 0
            Nmax = 255
            if Omin != Omax:
                #arr[...,i] -= minval
                #arr[...,i] *= (255/(maxval-minval))
                
                #arr = (1/(1+np.exp(-np.true_divide(arr-mval, maxval))))*255
                arr = (arr-Omin)*((Nmax-Nmin)/(Omin-Omax))+Nmin
                
        return arr
    

    def activate_Areadraw(self):
        self.canvas.bind("<Motion>", self.start_draw)
        self.canvas.bind("<Button-1>", self.drawArea)
        #self.canvas.focus_set()
        #self.master.is_draw_state = True
        #self.shown_image = None
        print("Hehehe ready to draw")

    def activate_ROIdraw(self):
        self.canvas.bind("<Motion>", self.start_draw)
        self.canvas.bind("<Button-1>", self.drawROI)
        #self.canvas.focus_set()
        #self.master.is_draw_state = True
        #self.shown_image = None
        print("Hehehe ready to draw")

        
    def deactivate_draw(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")

        #self.master.is_draw_state = False
    


    def show_image(self, img=None, C=1000):#C is the center of the window
        #self.clear_canvas()

        # if img is None:
        #     image = self.originalImg.copy()
        # else:
        #     image = img

        image = img
        height, width= image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))
        
        
        #print(image)
        new_width =    self.scale*new_width
        new_height =   self.scale*new_height
        self.shown_image = cv2.resize(image, (new_width, new_height))
        NormImg = self.normalize(self.shown_image, c=C)
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(NormImg.astype('uint8')))
        #print(self.shown_image )

        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)
        
    def start_draw(self, event):
        self.x = event.x
        self.y = event.y

    def drawArea(self, event):
        # self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
        #                                              fill="red", capstyle=ROUND, smooth=True))
        d = 100*self.scale
        print(d)
        self.draw_ids.append(self.canvas.create_rectangle(self.x-d/2, self.y-d/2, self.x +d/2, self.y+d/2, width=2, outline='red'))
        
        #print(self.x, self.y)
        
        # cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
        #          (int(event.x * self.ratio), int(event.y * self.ratio)),
        #          (0, 0, 255), thickness=int(self.ratio * 2),
        #          lineType=8)
        self.imcrop[0][0]= int((self.x/self.scale)-100/2)
        self.imcrop[0][1]= int((self.y/self.scale)-100/2)
        self.imcrop[2][0]= int((100))
        #print(self.imcrop)
        


        self.x = event.x
        self.y = event.y
    
    def drawROI(self, event):
        # self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
        #                                              fill="red", capstyle=ROUND, smooth=True))
        d = 50*self.scale
        self.draw_ids.append(self.canvas.create_rectangle(self.x-d/2, self.y-d/2, self.x +d/2, self.y+d/2, width=2, outline='green'))
        self.imcrop[1][0]= int((self.x/self.scale)-50/2)
        self.imcrop[1][1]= int((self.y/self.scale)-50/2)
        self.imcrop[2][1]= int((50))
        #print(self.imcrop)
        #print(self.x, self.y)
        
        # cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
        #          (int(event.x * self.ratio), int(event.y * self.ratio)),
        #          (0, 0, 255), thickness=int(self.ratio * 2),
        #          lineType=8)
        


    #     self.x = event.x
    #     self.y = event.y
    
    

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_draw(self):
        self.canvas.delete(self.draw_ids)
    