#! /usr/local/bin/proxychains4 python3.6
"""
desc  : download vedios from youtube via proxy agent.
author: Bodhi wang
mail  : jyxz5@qq.com
date  : 2017.9.11


Remove proxy agent and modify the call to pytube.
modified by Bodhi, 2018.3.23

Check if target file exists. If so, skip its download process.
modified by Bodhi, 2018.3.26
"""
import sys
import time
import os
import re
from functools import wraps
from pytube import YouTube
from pathlib import Path


urls = (
        'https://www.youtube.com/watch?v=H0SbnlDsdAc',
        'https://www.youtube.com/watch?v=McVxUs7d7ok',
        'https://www.youtube.com/watch?v=5obRgTyTy7Q',
        'https://www.youtube.com/watch?v=ZKZW2M1C7jU',
        'https://www.youtube.com/watch?v=AjgD3CvWzS0',
        'https://www.youtube.com/watch?v=JmiKWTRoiMk',
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
        print("[TIME       ] {0}".format(getHumanTime(end-start)))
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
        print("[ERROR      ] {0}".format(str(e)).encode("utf-8"))
        return -1

    pattern = r'[\/.:*?"<>|]+'
    regex = re.compile(pattern)
    filename = regex.sub('',yt.title).\
                     replace('\'','').replace('\\','')+".mp4"

    p=Path(local_dir)
    fp = p / filename
    if fp.exists():
        print("[SKIP       ] {0}".format(filename))
        return 0
    
    try:   
        print("[DOWNLOAD   ] {0}".format(filename))
        yt.streams.filter(subtype='mp4',progressive=True).first().download(local_dir)
        print("[DONE       ] {0}".format(filename))
    except Exception as e:
        print("[ERROR      ] {0}".format(str(e)).encode("utf-8"))
        return -1
   
    return 1


print("")
local_dir = os.path.join(os.getcwd(),"youtube")
#print("local_dir=",local_dir)
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
    print("[URL        ] {0}".format(url))
    ret = download(url, local_dir)
    if (ret > 0):
        file_count += ret
    print("")

end = time.time()
elapsed = end - start
print("")
print("Total {0} file(s) downloaded into directry {1}".format(file_count, local_dir))
print("Elapsed time {0}".format(getHumanTime(elapsed)))

exit(0)
