#! /usr/bin/python3

# -*- coding: utf-8 -*-

import time, threading
import random, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import xticks, yticks

class GraphsClass():
    def __init__(self, len_history):
        self.fig = plt.figure()

        self.dates = ["Last" for i in range(len_history)]
        self.money = [0 for i in range(len_history)]
        self.wood = [0 for i in range(len_history)]
        self.rock = [0 for i in range(len_history)]
        self.number_of_graphs = 0
        self.len_history = len_history
        os.system("rm -f /home/pi/demons/WarTrade/static/graphs/*")

    def new_element(self, money, wood, rock, date):
        if(date != self.dates[len(self.dates)-1]):
            self.money.append(money)
            self.money.pop(0)

            self.wood.append(wood)
            self.wood.pop(0)

            self.rock.append(rock)
            self.rock.pop(0)

            self.dates.append(date)
            self.dates.pop(0)

    def save_new_graphs(self):
        self.number_of_graphs+=1

        plt.clf()

        plt.plot(self.money, color = 'yellow', linestyle = 'solid', label = 'money')
        plt.plot(self.wood, color = 'green', linestyle = 'solid', label = 'wood')
        plt.plot(self.rock, color = 'blue', linestyle = 'solid', label = 'rock')

        xticks(range(self.len_history), self.dates)
        #yticks(range(10), [(i+1)*10 for i in range(10)])
        plt.xlabel('Дата')
        plt.ylabel('Цена')

        self.fig.savefig('static/graphs/'+str(self.number_of_graphs)+'.png')
        return self.number_of_graphs

