"""
desc  : download vedios from youtube via proxy agent.
author: Bodhi wang
mail  : bodwang@deloitte.com.cn
date  : 2017.9.11
"""
import urllib.request
import urllib.error
import sys
import time
import os
#from functools import wraps
from pytube import YouTube

proxy = {'http':'http://127.0.0.1:1080',
         'https':'https://127.0.0.1:1080'}
urls = (
        "https://www.youtube.com/watch?v=NBliyFXnWeo&list=PLGVZCDnMOq0oieXy92cJBwSirA3G2MCU1",
        "https://www.youtube.com/watch?v=UNEZJUbJkog",
        "https://www.youtube.com/watch?v=Cnfj6QCGLyA",
        'https://www.youtube.com/watch?v=VoNai5i0qOI',
        'https://www.youtube.com/watch?v=ABy95341Dto',
        'https://www.youtube.com/watch?v=VoNai5i0qOI',
        'https://www.youtube.com/watch?v=W41IFXbB5-M',
        'https://www.youtube.com/watch?v=6ixhN9umyp4',
        'https://www.youtube.com/watch?v=v1QY8aAWYc4',
        'https://www.youtube.com/watch?v=2j0My82eesY',
        'https://www.youtube.com/watch?v=rNdr7yAv-xg',
        'https://www.youtube.com/watch?v=X2SSLOlsJFI',
        'https://www.youtube.com/watch?v=tByJMiQp-IM',
        'https://www.youtube.com/watch?v=Ju86mknumYM',
        'https://www.youtube.com/watch?v=ABy95341Dto',
        'https://www.youtube.com/watch?v=62Y7BXIuX6Y',
        'https://www.youtube.com/watch?v=3xQTJi2tqgk&list=PLt9Zf_aPaQ4K07I5QFHEu3rFqgzYwpsAr',
        'https://www.youtube.com/watch?v=5-oyXC0iV_4',
        'https://www.youtube.com/watch?v=SSu00IRRraY',
        'https://www.youtube.com/watch?v=Tq6rCWPdXoQ',
        'https://www.youtube.com/watch?v=MGx9aUVT7HU',
        'https://www.youtube.com/watch?v=To3YL92HZyc&list=PLXO45tsB95cKKyC45gatc8wEc3Ue7BlI4',
          )


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start, "Secs")
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
        #video = yt.get('mp4', '720p')
        video = yt.get('mp4', '1080p')
    except Exception:  # Sorts videos by resolution and picks the highest quality video if a 1080p video doesn't exist
        video = sorted(yt.filter("mp4"), key=lambda video: int(video.resolution[:-1]), reverse=True)[0]

    try:
        video.download(local_dir)
        print("successfully downloaded", yt.filename)
        return 1
    except OSError:
        print(yt.filename, "already exists in this {0}! Skipping video...".format(local_dir))
        return 0


#local_dir = os.getcwd() + "/youtube"os.path.join(os.getcwd,)
local_dir = os.path.join(os.getcwd(),"youtube")
print("local_dir=",local_dir)
# make local_dir if dir specified doesn't exist
try:
    os.makedirs(local_dir, exist_ok=True)
except OSError as e:
    print(e.reason)
    exit(1)

proxy_support = urllib.request.ProxyHandler(proxy)
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

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