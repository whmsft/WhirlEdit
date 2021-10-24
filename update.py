import os
import sys
import urllib
import zipfile
import platform
import requests
import requests
import threading
import tkinter as tk
from tkinter import ttk
from pathlib import Path

latestver = urllib.request.urlopen("https://github.com/whmsft/whmsft/raw/main/projects/whirledit.latest-version.txt").read().decode()

updatelink = f'\rhttps://whmsft.github.io/releases/whirledit-{latestver}-{platform.platform()}.zip'

def printProgressBar(iteration, total, length=50,fill = '█', printEnd = "\r"):
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\rDownloading release {latestver} |{bar}| {round(iteration/total*100,1)}% [{pgr[num]}]', end = printEnd)

def getfile(file):
    global pgr, num
    pgr = ['|','/','-','\\']
    url = file
    local_filename = "./"+file.split("/")[-1]
    num = 0
    response = requests.head(file)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            iterr = 0
            printProgressBar(0,int(response.headers['content-length']))
            for chunk in r.iter_content(chunk_size=8192):
                printProgressBar(iterr+8192,int(response.headers['content-length']))
                iterr+=8192
                if num == 3:
                    num = 0
                else:
                    num += 1
                f.write(chunk)
    zipfile.ZipFile(local_filename,'r').extractall(Path(Path(__file__).parent.resolve()))

def download_latest(url=''):
    local_filename = "./"+url.split("/")[-1]
    size=response.headers['content-length']
    pbar['maximum'] = int(size)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        f=open(local_filename,'wb')
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar['value'] += len(chunk)
    f.close()
    text['text'] = 'Installing'
    zipfile.ZipFile(local_filename,'r').extractall(Path(Path(__file__).parent.resolve()))
    text['text'] = 'Done'
    root.destroy()
    exit()
    sys.exit()

if not latestver.split()[0] == open('currentversion.txt','r').read().split()[0]:
    if '--gui' not in sys.argv:
        getfile(updatelink)
        print('Upgraded WhirlEdit to {}'.format(latestver))
        exit()
    else:
        root = tk.Tk()
        root.wm_attributes("-topmost",1)
        response = requests.head(updatelink)
        text = tk.Label(root,text='Downloading',font='segoe\ ui 20')
        text.pack()
        pbar = ttk.Progressbar(root,maximum=response.headers['content-length'],length=250)
        pbar.pack(side='left', pady=5,padx=5)
        cancel=tk.Button(root,text=' x ', bg='red',fg='white', activeforeground='white', activebackground='red',borderwidth=0,relief='flat', command=lambda:exec('root.destroy()\nexit\nsys.exit()'))
        cancel.pack(side='left',padx=5,pady=5)
        root.after(50,lambda:threading.Thread(target=download_latest,kwargs={"url":updatelink}, daemon=True).start())
        root.mainloop()
else:
    print('Already at the latest version {}'.format(latestver))
    exit()
