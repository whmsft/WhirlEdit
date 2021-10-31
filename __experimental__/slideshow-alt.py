import tkinter as tk
from PIL import Image, ImageTk
import time
import sys
import os

class HiddenRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #hackish way, essentially makes root window
        #as small as possible but still "focused"
        #enabling us to use the binding on <esc>
        self.wm_geometry("0x0+0+0")

        self.window = MySlideShow(self)
        self.window.startSlideShow()


class MySlideShow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        #remove window decorations 
        self.overrideredirect(True)

        #save reference to photo so that garbage collection
        #does not clear image variable in show_image()
        self.persistent_image = None
        self.imageList = []
        self.pixNum = 0

        #used to display as background image
        self.label = tk.Label(self)
        self.label.pack(side="top", fill="both", expand=True)

        self.getImages()

    def getImages(self):
        '''
        Get image directory from command line or use current directory
        '''
        if len(sys.argv) == 2:
            curr_dir = sys.argv[1]
        else:
            curr_dir = '.'

        for root, dirs, files in os.walk(curr_dir):
            for f in files:
                if f.endswith(".png") or f.endswith(".jpg") or f.endswith('.gif'):
                    img_path = os.path.join(root, f)
                    print(img_path)
                    self.imageList.append(img_path)

    def startSlideShow(self, delay=1): #delay in seconds
        myimage = self.imageList[self.pixNum]
        self.pixNum = (self.pixNum + 1) % len(self.imageList)
        self.showImage(myimage)
        #its like a callback function after n seconds (cycle through pics)
        self.after(delay*1000, self.startSlideShow)

    def showImage(self, filename):
        image = Image.open(filename)  

        img_w, img_h = image.size
        scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()
        width, height = min(scr_w, img_w), min(scr_h, img_h)
        image.thumbnail((width, height), Image.ANTIALIAS)

        #set window size after scaling the original image up/down to fit screen
        #removes the border on the image
        scaled_w, scaled_h = image.size
        self.wm_geometry("{}x{}+{}+{}".format(scaled_w,scaled_h,0,0))
        
        # create new image 
        self.persistent_image = ImageTk.PhotoImage(image)
        self.label.configure(image=self.persistent_image)


slideShow = HiddenRoot()
slideShow.bind("<Escape>", lambda e: slideShow.destroy())  # exit on esc
slideShow.mainloop()
