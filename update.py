import py7zr
from urllib import request
import requests
import sys, os
import tkinter as tk
from tkinter import ttk
import platform
from tkinter.messagebox import *
import threading
"""
import os
import time
import sys
import urllib
import platform
import requests
import requests
import threading
import tkinter as tk
from tkinter import tt
from pathlib import Path

latestver = urllib.request.urlopen("https://github.com/whmsft/whmsft/raw/main/projects/whirledit.latest-version.txt").read().decode().split()[0]
updatelink = 'https://whmsft.github.io/releases/whirledit-{}-{}.7z'.format(latestver,platform.platform().split('-')[0].lower())
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
    py7zr.SevenZipFile(local_filename, mode='r').extractall(path="./")
    os.remove(local_filename)

def download_latest(url=''):
    local_filename = "./"+url.split("/")[-1]
    size=response.headers['content-length']
    pbar['maximum'] = int(size)
    text['text'] = 'Downloading..'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        f=open(local_filename,'wb')
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar['value'] += len(chunk)
    f.close()
    text['text'] = 'Installing..'
    py7zr.SevenZipFile(local_filename, mode='r').extractall(path="./")
    os.remove(local_filename)
    text['text'] = 'Done!'
    time.sleep(0.5)
    sys.exit()
"""
def download_latest(url=''):
    local_filename = "./"+url.split("/")[-1]
    size=response.headers['content-length']
    pbar['maximum'] = int(size)
    dtext['text'] = 'Downloading..'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        f=open(local_filename,'wb')
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar['value'] += len(chunk)
    f.close()
    dtext['text'] = 'Installing..'
    py7zr.SevenZipFile(local_filename, mode='r').extractall(path="./")
    os.remove(local_filename)
    sys.exit()
def check_for_update(*args):
    global response, pbar, proot, dtext
    latestver = request.urlopen("https://github.com/whmsft/whmsft/raw/main/projects/whirledit.latest-version.txt").read().decode().split()[0]
    updatelink = 'https://whmsft.github.io/releases/whirledit-{}-{}.7z'.format(latestver,platform.platform().split('-')[0].lower())
    if not latestver.split()[0] == open('currentversion.txt','r').read().split()[0]:
        choice_to_update = askyesnocancel('Update','New version {} available.\nDownload and install?\nNOTE: close WhirlEdit.exe else installation will not finish \n also, once started, the update can\'t be cancelled'.format(latestver))
        if choice_to_update:
                proot = tk.Toplevel()
                proot.title('WhirlEdit Updater')
                proot.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
                dtext = tk.Label(proot,text='Housekeeping..',font='segoe\ ui 20')
                dtext.pack()
                dtext['text'] = 'Finding info about update'
                response = requests.head(updatelink)
                pbar = ttk.Progressbar(proot,maximum=response.headers['content-length'],length=250)
                pbar.pack(side='left', pady=5,padx=5)
                proot.after(50,lambda:threading.Thread(target=download_latest,kwargs={"url":updatelink}, daemon=True).start())
                proot.mainloop()
    else:
        showinfo('Update','Already at the latest version')
check_for_update()
