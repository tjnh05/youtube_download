#! /usr/local/bin/proxychains4 -q python3.6
"""
desc  : download vedios from youtube via proxy agent.
author: Bodhi wang
mail  : jyxz5@qq.com
date  : 2017.9.11


Remove proxy agent and modify the call to pytube.
modified by Bodhi, 2018.3.23
"""
import sys
import time
import os
from functools import wraps
from pytube import YouTube

urls = (
        'https://www.youtube.com/watch?v=Xi52tx6phRU',
        'https://www.youtube.com/watch?v=Tq6rCWPdXoQ',
        'https://www.youtube.com/watch?v=MGx9aUVT7HU',
        'https://www.youtube.com/watch?v=To3YL92HZyc&list=PLXO45tsB95cKKyC45gatc8wEc3Ue7BlI4',
          )

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, getHumanTime(end-start))
        return result
    return wrapper

def getHumanTime(sec):
    if sec >= 3600:  # Converts to Hours
        return '{0:d} hour(s)'.format(int(sec / 3600))
    elif sec >= 60:  # Converts to Minutes
        return '{0:d} minute(s)'.format(int(sec / 60))
    else:            # No Conversion
        return '{0:d} second(s)'.format(int(sec))

@timethis
def download(url, local_dir):
    try:
        yt=YouTube(url)
    except Exception as e:
        print("Error {0}".format(str(e)).encode("utf-8"))
        return -1

    try:
        yt.streams.filter(subtype='mp4',progressive=True).first().download(local_dir)
        print("successfully downloaded", yt.title)
        return 1
    except OSError:
        print(yt.title, "already exists in this {0}! Skipping video...".format(local_dir))
        return 0


local_dir = os.path.join(os.getcwd(),"youtube")
print("local_dir=",local_dir)
# make local_dir if dir specified doesn't exist
try:
    os.makedirs(local_dir, exist_ok=True)
except OSError as e:
    print(e.reason)
    exit(1)

start = time.time()

file_count = 0
for url in urls:
    url_start = time.time()
    print("Download for url:", url)
    ret = download(url, local_dir)
    if (ret > 0):
        file_count += ret
    print("")

end = time.time()
elapsed = end - start
print("Total {0} file(s) have been downloaded into directry {1}!".format(file_count, local_dir))
print("Elapsed time {0}.".format(getHumanTime(elapsed)))

exit(0)
