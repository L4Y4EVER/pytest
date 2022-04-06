# This is a sample Python script.

import json
import os
import time

import pandas as pd
import datetime as dt
# import numpy as np


# 获取有关发消息之间差值方法
def make_everyday_data():
    dateDict = []

    # 3月25日开始 time.
    for info in os.listdir('D:/downloads/dataCSV'):
        domain = os.path.abspath('D:/downloads/dataCSV')
        fn = os.path.join(domain, info)
        content = pd.read_csv(fn,encoding='ISO-8859-1',names=['cyjid'],header=0)
        ids = set()
        for i in range(len(content)):
            ids.add(str.split(content['cyjid'][i], '@')[0])
        dateDict.append(ids)

    date = []
    nl = []
    newl = []
    new_ratiol = []
    onel = []
    one_ratiol = []
    threel = []
    three_ratiol = []
    sevenl = []
    seven_ratiol = []
    thirtyl = []
    thirty_ratiol = []

    # 留存1 日 3日 7日 30日 留存人数 留存率 每日新增 新增率
    d = dt.date.today().replace(2022,3,3)
    l = len(dateDict)
    for index in range(l):
        new = 0
        new_ratio = 0
        one = 0
        one_ratio = 0
        three = 0
        three_ratio = 0
        seven = 0
        seven_ratio = 0
        thirty = 0
        thirty_ratio = 0
        now = dateDict[index]
        n = len(now)
        if((index - 1 ) >= 0):
            y = dateDict[index - 1]
            for a in iter(now):
                if(not (a in y)):
                    new += 1
            new_ratio = new / len(y) * 100

        if((index + 1) < l):
            t = dateDict[index + 1]
            for a in iter(t):
                if(a in now):
                    one += 1
            one_ratio = one / n * 100

        if((index + 2) < l):
            t1 = dateDict[index + 2]
            for a in iter(t1):
                if(a in now):
                    three += 1
            three_ratio = three / n * 100

        if((index + 6) < l):
            t2 = dateDict[index + 6]
            for a in iter(t2):
                if(a in now):
                    seven += 1
            seven_ratio = seven / n * 100

        if((index + 29) < l):
            t3 = dateDict[index + 29]
            for a in iter(t3):
                if(a in now):
                    thirty += 1
            thirty_ratio = thirty / n * 100

        date.append(d.strftime('%Y-%m-%d'))
        nl.append(n)
        newl.append(new)
        new_ratiol.append(new_ratio)
        onel.append(one)
        one_ratiol.append(one_ratio)
        threel.append(three)
        three_ratiol.append(three_ratio)
        sevenl.append(seven)
        seven_ratiol.append(seven_ratio)
        thirtyl.append(thirty)
        thirty_ratiol.append(thirty_ratio)
        d = d + dt.timedelta(1)

    dataframe = pd.DataFrame(
        {'日期': date, '日活':nl,'新增人数': newl, '日留存人数': onel,'三日留存人数': threel,'七日留存人数': sevenl,'三十日留存人数': thirtyl,
         '新增比例': new_ratiol, '日留存比例': one_ratiol, '三日留存比例': three_ratiol, '七日留存比例': seven_ratiol, '三十日留存比例': thirty_ratiol})
    dataframe.to_csv("D:/work/log/test2.csv", index=False, sep=',')

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




