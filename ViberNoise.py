# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:26:05 2019

@author: 1
"""
from datetime import datetime
#Позволяет распознавать дату, записанную на русском языке
import locale

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D

locale.setlocale(locale.LC_ALL,'')
#Словари хороших и плохих слов
GoodWords = {'домашн': 4,'задан': 5, 'работ' : 4, 'задал' : 3,'геометр' : 2,'англ' : 4,'алгебр' : 4,'русск' : 4,'литерат' : 3,'физик' : 2,'инф' : 6,'объявлен' : 1,'дз' : 5,'домашк' : 5,'параграф' : 1,'завтра' : 1,'учимся' : 2,'долги' : 3,'принести' : 2,'надо' : 4,'нужно' : 3,'обязятельн' : 4,'втор' : 4,'паре' : 3,'пара' : 1,'фотосообщение' : 1,'§' : 4,'!' : 1,'гоегр' : 2,'биолог' : 2,'запис' : 2,'асу' : 1,'рсо' : 1,'вопрос' : 3,'письм' : 3,'голосовое':3,}
BadWords = {'лень' : -2,'пофиг' : -3,'фортнайт' : -5,'дота' : -5,'хелп' : -4,'спишу' : -4,'помогите' : -1,'ненавижу' : -2,'капец' : -2,'хз' : -3,}

#Словарь дней недели
WeekDays = {}
DailyCount = {}
#Словарь весов по часам
Weights = {}
HourlyCount = {}
#Функция разбирает сообщение по составлюящим и определяет вес всех слов
def WeightFromText(text):
    #разберём строчку на дату и время, имя отправителя и сообщение
    DTraw,_,NMraw = text.partition(']')
    SenderName,_,Message= NMraw.partition(':')
    Message = Message.strip()
    SenderName = SenderName.strip()
    #отформатируем дату для последующей обработки
    DTraw = DTraw[1:].strip()
    DTraw = DTraw.replace('ря', 'рь') 
    DTraw = DTraw.replace('та', 'т')
    DTraw = DTraw.replace('ля', 'ль')
    DTraw = DTraw.replace('ня', 'нь')
    DTraw = DTraw.replace('ая', 'ай')
    
    #превращаем строчку DTraw в объект типа datetime
    DTobj = datetime.strptime(DTraw, '%d %B %Y г. %H:%M')
    
    words = Message.lower().split()
    
    WeightSum = 0
    #считаем суммарный вес слов в сообщении
    for word in words:
        for GW in GoodWords:
            if word.startswith(GW):
                WeightSum += GoodWords[GW]
        for BW in BadWords:
            if word.startswith(BW):
                WeightSum += BadWords[BW]
                
    #возвращаем значения веса сообщения,день недели,час отправки сообщения
    return (WeightSum, DTobj.strftime('%A'),DTobj.hour)

#откроем файл с сообщениями
ChatFile = open('Chat_copy.txt',encoding='utf-8')
Chat_lines = ChatFile.readlines()
ChatFile.close()
#если сообщение не занимает больше 1 строчки то мы разбиваем на несколько частей и проставляем время и отправителя предыдушей строчки 
for i in range(len(Chat_lines)):
    if not Chat_lines[i].startswith('['):
        prev = Chat_lines[i-1].split(':')
        prev = prev[0]+':'+prev[1]+': '
        Chat_lines[i]=prev+Chat_lines[i]

#применяем функцию к каждому сообщению и определяем день недели час и вес записывая в новые словари
weight = 0
#словарь весов по часам по дням недели
WeekW = {'понедельник':[0]*24,'вторник':[0]*24,'среда':[0]*24,'четверг':[0]*24,'пятница':[0]*24,'суббота':[0]*24,'воскресенье':[0]*24}
MessW = {'понедельник':[0]*24,'вторник':[0]*24,'среда':[0]*24,'четверг':[0]*24,'пятница':[0]*24,'суббота':[0]*24,'воскресенье':[0]*24}
AveW  = {'понедельник':[0]*24,'вторник':[0]*24,'среда':[0]*24,'четверг':[0]*24,'пятница':[0]*24,'суббота':[0]*24,'воскресенье':[0]*24}
for line in Chat_lines:
    w,d,h = WeightFromText(line)
    weight += w
    if not d in WeekDays:
        WeekDays[d]=w
        DailyCount[d]=1
    else:
        WeekDays[d]+=w
        DailyCount[d]+=1
    if not h in Weights:
        Weights[h] = w
        HourlyCount[h]=1
    else:
        Weights[h] += w
        HourlyCount[h]+=1
    WeekW[d][h]+=w
    MessW[d][h]+=1
    AveW[d][h]= WeekW[d][h]/MessW[d][h]

#составляем два списка, где находятся час и вес сообщений отправленных за этот час
lHours = []
lWeights = []
lHCount = []
lHAverage = []
for i in range (0,24):
    lHours = lHours + [i] 
    if not i in Weights:
        lWeights += [0]
        lHCount += [0]
        lHAverage += [0]
    else:
        lWeights += [Weights[i]]
        lHCount += [HourlyCount[i]]
        lHAverage += [Weights[i]/HourlyCount[i]]

tDays = ('понедельник','вторник','среда','четверг','пятница','суббота','воскресенье')
lDaysW = []
lDCount = []
lDAverage = []
for day in tDays:
    lDaysW += [WeekDays[day]]
    lDCount += [DailyCount[day]]
    lDAverage += [WeekDays[day]/DailyCount[day]]

#Превращаем списки и кортежи в массивы для создания графиков 
#с использованием модулей NumPy и Matplotlib
def Graph(x,y,name):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.xticks(np.arange(len(x)),x,rotation=90)
    fig.savefig(name + '.png')



for day in tDays:
    Graph(lHours,WeekW[day],day)

Graph(lHours,lWeights,'hours')
Graph(lHours,lHCount,'hourly_messages')
Graph(lHours,lHAverage,'hourly_average')
Graph(tDays,lDaysW,'days')
Graph(tDays,lDCount,'daily_messages')
Graph(tDays,lDAverage,'daily_average')



fig= plt.figure()
ax = fig.gca(projection='3d')
x,y = np.meshgrid(np.array(lHours),np.arange(0,7,1))
z = np.array([[i for i in WeekW[j]] for j in tDays])
ax.plot_surface(x,y, z,cmap=cm.coolwarm)
#Сохраняем его в файл
fig.savefig('3Dproj.png')


