# -*- coding:utf-8 -*-

import threadpool
import time
import requests as curl
import os
import glob
import re


def download1(url):
    file_path = os.path.basename(url)
    if os.path.exists(file_path):
        return
    r = curl.get(url, stream=True)
    print(url, r.status_code)
    f1 = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f1.write(chunk)
    f1.close()


def download2(src):
    if src.startswith("http"):
        return

    dir_path = os.path.dirname(src)
    if not os.path.exists(dir_path):
        ret = os.mkdir(dir_path)
        if not ret:
            print("dir  %s is not create" % src)

    file_url = "http://218.28.125.161/chan/%s" % (src,)
    file_path = src

    # if os.path.exists(file_path):
    #     return
    print(file_url)
    r = curl.get(file_url, stream=True)
    if not r.status_code == 200:
        print(r.status_code)
        return
    f1 = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f1.write(chunk)
    f1.close()


if __name__ == '__main__':
    # urls = ["http://218.28.125.161/chan/%03d.html" % i for i in range(1, 109)]

    # pool = threadpool.ThreadPool(2)
    # requests = threadpool.makeRequests(download1, urls)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()

    pool = threadpool.ThreadPool(5)
    files = glob.glob("*.html")
    for file_name in files:
        with open(file_name, 'r') as f:
            buf = f.read(1024 * 1024 * 1024)
            match = re.findall("src=\"([^\"]+)", buf)
            if match:
                requests = threadpool.makeRequests(download2, match)
                [pool.putRequest(req) for req in requests]
                pool.wait()
