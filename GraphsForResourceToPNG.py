#! /usr/bin/python3

# -*- coding: utf-8 -*-

import base64
from io import BytesIO

import time, threading 
import random, os, MySQLdb
import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3
from pylab import xticks, yticks

class GraphsClass():
    def __init__(self, len_history):
        self.fig = plt.figure()

        self.dates = ["Last" for i in range(len_history)]
        self.gold = [0 for i in range(len_history)]
        self.wood = [0 for i in range(len_history)]
        self.rock = [0 for i in range(len_history)]
        self.number_of_graphs = 0
        self.len_history = len_history

        self.base = MySQLdb.connect("192.168.32.10","platon","maker","WarTrade")
        self.cursor = self.base.cursor()
        self.cursor.execute("TRUNCATE TABLE ResourcesTrend")

        self.buf = BytesIO()
        self.fig.savefig(self.buf, format="png")
        self.data = base64.b64encode(self.buf.getbuffer()).decode("ascii")

        os.system("rm -f /home/pi/demons/WarTrade/static/graphs/*")

    def NewElement(self, gold, wood, rock, DateMini, DateFull):
        if(DateMini != self.dates[len(self.dates)-1]):
            self.gold.append(gold)
            self.gold.pop(0)
            self.wood.append(wood)
            self.wood.pop(0)
            self.rock.append(rock)
            self.rock.pop(0)
            self.dates.append(DateMini)
            self.dates.pop(0)

            self.cursor.execute("INSERT INTO ResourcesTrend(date, gold, wood, rock) VALUES ('{0}', '{1}', '{2}', '{3}')".format(DateFull, gold, wood, rock))
            self.base.commit()

            self.number_of_graphs+=1

            plt.clf()
            plt.plot(self.gold, color = 'orange', linestyle = 'solid', label = 'gold')
            plt.plot(self.wood, color = 'green', linestyle = 'solid', label = 'wood')
            plt.plot(self.rock, color = 'blue', linestyle = 'solid', label = 'rock')
            xticks(range(self.len_history), self.dates)
            #yticks(range(10), [(i+1)*10 for i in range(10)])
            plt.xlabel('Дата')
            plt.ylabel('Цена')

            #self.fig.savefig('static/graphs/'+str(self.number_of_graphs)+'.png')
            self.buf = BytesIO()
            self.fig.savefig(self.buf, format="png")
            self.data = base64.b64encode(self.buf.getbuffer()).decode("ascii")
    def GetActualGraph(self):
        return self.data

