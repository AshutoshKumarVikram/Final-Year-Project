import smtplib
from tkinter import *
from tkinter import messagebox
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

root = Tk()
label_1 = Label( root, text="Enter source of the video feed", font=("Arial Bold", 10) )
root.title( "Video Processing and Analysis" )
root.geometry( "400x300" )
label_2 = Label( root, text="Enter User Details" )
label_3 = Label( root, text="Email" )
label_4 = Label( root, text="Password" )

entry_1 = Text( root, height=1, width=18 )
entry_2 = Text( root, height=1, width=18 )
entry_3 = Text( root, height=1, width=18 )

label_1.grid( row=0, sticky=E )
label_2.grid( row=1, sticky=W )
label_3.grid( row=2, sticky=E )
label_4.grid( row=3, sticky=E )

entry_1.grid( row=0, column=1 )
entry_2.grid( row=2, column=1 )
entry_3.grid( row=3, column=1 )

c = Checkbutton( root, text="Check if you want to send the alert" )
c.grid( column=0, row=9, columnspan=2 )


def clicked():
    messagebox.showinfo( 'Alert', 'Feed analysis started, alert will be sent to your mail if security is breached' )
    # change the video source

    src = entry_1.get( "1.0", "end-1c" )
    cap = cv2.VideoCapture( src )
    fgbg = cv2.createBackgroundSubtractorMOG2()

    looper, image = cap.read()
    count = 0
    looper = True
    size = 600, 400
    for count in range( 0, 100 ):
        looper, image = cap.read()
        print( 'Read a new frame: ', looper )
        count + 1
        if (count == 10):
            cv2.imwrite( "frame%d.jpg" % count, image )
            img = Image.open( "frame%d.jpg" % count )
            img2 = img.rotate( 90 )
            img2.thumbnail( size, Image.ANTIALIAS )
            img2.save( "img2.jpg" )
            s = smtplib.SMTP( 'smtp.gmail.com', 587 )
            s.starttls()
            
            email = entry_2.get( "1.0", "end-1c" )
            pwd = entry_3.get( "1.0", "end-1c" )
            
            s.login(email, pwd )
            message = "There is a movement in the area"
            s.sendmail(email, pwd, message )
            s.quit()
            print( "Screenshot success\n" )
            break

    while (1):
        ret, frame = cap.read()
        fgmask = fgbg.apply( frame )
        imS = cv2.resize( frame, (800, 600) )
        imS2 = cv2.resize( fgmask, (800, 600) )
        cv2.imshow( 'fgmask', imS )
        cv2.imshow( 'frame', imS2 )
        k = cv2.waitKey( 30 ) & 0xff
        if k == 27:
            break


btn = Button( root, text="Start Analyzing", command=clicked )
btn.grid( row=6, column=1 )

root.mainloop()
