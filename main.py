# This is a sample Python script.

import json
import os
import time

import pandas as pd
import datetime as dt
# import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# 获取有关发消息之间差值方法
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

# 获取有关发消息各个指标数据
def get_data():
    f = open('D:/work/log/downloaded_data.txt',encoding='UTF-8')
    hjbp = set()
    hjsj = set()
    hjtm = set()
    pchat = set()
    cyj = set()

    date = []
    bplist = []
    sjlist = []
    tmlist = []
    plist = []
    cyjlist = []

    t = "2022-03-23"
    # '2022-03-23_08:44:10.165 RCV from:tl_12|0|120036780@im.jia.changyou.com/CYJ'
    for line in f:
        jSon = json.loads(line)
        content = jSon['content']
        nt = time.strftime('%Y-%m-%d', time.localtime(int(jSon['__time__'])))
        if not(t.__eq__(nt)):
            print("now data:",t)
            print("hjbp:", len(hjbp))
            print("hjsj:", len(hjsj))
            print("hjtm:", len(hjtm))
            print("pchat:", len(pchat))
            print("cyj:", len(cyj))
            date.append(t)
            bplist.append(len(hjbp))
            sjlist.append(len(hjsj))
            tmlist.append(len(hjtm))
            plist.append(len(pchat))
            cyjlist.append(len(cyj))
            t = nt
            hjbp.clear()
            hjsj.clear()
            hjtm.clear()
            pchat.clear()
            cyj.clear()

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
    print("end------date",t)
    print("hjbp:", len(hjbp))
    print("hjsj:", len(hjsj))
    print("hjtm:", len(hjtm))
    print("pchat:", len(pchat))
    print("cyj:", len(cyj))
    date.append(t)
    bplist.append(len(hjbp))
    sjlist.append(len(hjsj))
    tmlist.append(len(hjtm))
    plist.append(len(pchat))
    cyjlist.append(len(cyj))
    # 字典中的key值即为csv中列名 输出到csv
    dataframe = pd.DataFrame({'date': date, 'bpcount': bplist, 'sjcount': sjlist, 'tmcount': tmlist, 'pccount': plist, 'cyjcount': cyjlist})
    dataframe.to_csv("D:/work/log/test.csv", index=False, sep=',')


if __name__ == '__main__':
    get_data()




