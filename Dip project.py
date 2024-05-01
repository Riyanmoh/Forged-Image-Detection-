
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils

global grayA, grayB
global im1, im2

def select_image_1():
        global panelA, panelB
        global grayA, grayB
        global im1,im2

        path = tkFileDialog.askopenfilename()

        if len(path) > 0:
                
                image = cv2.imread(path)
                im1 = image
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edged = cv2.Canny(gray, 50, 100)

                grayA = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                
                image = Image.fromarray(image)
                edged = Image.fromarray(edged)

               
                image = ImageTk.PhotoImage(image)
                edged = ImageTk.PhotoImage(edged)

                
                if panelA is None or panelB is None:
                        
                        panelA = Label(image=image)
                        panelA.image = image
                        panelA.pack(side="left", padx=10, pady=10)

                
                else:
                        
                        panelA.configure(image=image)
                        
                        panelA.image = image
                        
def select_image_2():
       
        global panelA, panelB
        global grayA, grayB
        global im1,im2

     
        path = tkFileDialog.askopenfilename()

    
        if len(path) > 0:
        
                image = cv2.imread(path)
                im2 = image
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edged = cv2.Canny(gray, 50, 100)

                grayB = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(image)
                edged = Image.fromarray(edged)

               
                image = ImageTk.PhotoImage(image)
                edged = ImageTk.PhotoImage(edged)

                if panelA is None or panelB is None:
                      
                        panelB = Label(image=image)
                        panelB.image = image
                        panelB.pack(side="right", padx=10, pady=10)

                else:
                     
                        panelA.configure(image=image)
                        panelB.configure(image=edged)
                        panelA.image = image
                        panelB.image = edged

def check_image():
     
        global panelA, panelB
        global grayA, grayB
        global im1,im2
        score, diff = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
               
                cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 255), 2)

                
                image = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
                edged = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)
                
                image = Image.fromarray(image)
                edged = Image.fromarray(edged)
                
                image = ImageTk.PhotoImage(image)
                edged = ImageTk.PhotoImage(edged)
                panelA.configure(image=image)
                panelB.configure(image=edged)
                
                panelA.image = image
                panelB.image = edged

root = Tk()
panelA = None
panelB = None

btn = Button(root, text="Select Original image", command=select_image_1)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn2 = Button(root, text="Select Test image", command=select_image_2)
btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn3 = Button(root, text="Check", command=check_image)
btn3.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()
