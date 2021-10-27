import py7zr
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
from tkinter import ttk
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
updfile=open('./updfile.txt').read()
py7zr.SevenZipFile(updfile, mode='r').extractall(path="./")
os.remove('./updfile.txt')
os.remove(updfile)
