# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import time

import pandas as pd
import datetime as dt
import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def make_data():
    for info in os.listdir('D:/downloads/csv'):
        domain = os.path.abspath('D:/downloads/csv')
        fn = os.path.join(domain, info)
        content = pd.read_csv(fn,encoding='ISO-8859-1')
        max = 1
        min = 1
        for i in range(len(content)):
            stime = str(content['content'][i]).split(' ')[0].replace('_',' ')
            if 'nan' == stime:
                continue
            time = dt.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000
            if(i == 0):
                max = time
                min = time
                continue
            if(max < time):
                max = time
                continue
            if(time < min):
                min = time
                continue
        print(max - min)

def get_data():
    f = open('D:/work/log/downloaded_data.txt',encoding='UTF-8')
    hjbp = set()
    hjsj = set()
    hjtm = set()
    pchat = set()
    cyj = set()

    # '2022-03-23_08:44:10.165 RCV from:tl_12|0|120036780@im.jia.changyou.com/CYJ'
    for line in f:
        jSon = json.loads(line)
        content = jSon['content']
        time.strftime('%Y-%m-%d', time.localtime(int(jSon['__time__'])))
        # time.strftime()
        if content.__contains__('RCV from') and content.__contains__('|0|'):
            ujid = str.split(str.split(content, ";")[2], ":")[1]
            cyj.add(str.split(ujid,'@')[0])

        if content.__contains__('RCV from') and content.__contains__('groupchat'):
           if content.__contains__('hjbp'):
                hjbp.add(str.split(str.split(content,";")[0],"from:")[1])
           elif content.__contains__('hjsj'):
                hjsj.add(str.split(str.split(content, ";")[0], "from:")[1])
           elif content.__contains__('hjtm'):
                hjtm.add(str.split(str.split(content, ";")[0], "from:")[1])
           else:
               continue
        elif content.__contains__('RCV from') and content.__contains__('|0|') and content.__contains__('type:chat'):
            pchat.add(str.split(str.split(content, ";")[0], "from:")[1])
        else:
            continue

    print("hjbp:", len(hjbp),hjbp)
    print("hjsj:", len(hjsj),hjsj)
    print("hjtm:", len(hjtm),hjtm)
    print("pchat:", len(pchat),pchat)
    print("cyj:", len(cyj), cyj)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_data()
    # f = open('D:/work/log/downloaded_data.txt',encoding='UTF-8')





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
