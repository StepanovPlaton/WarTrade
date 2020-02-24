#! /usr/bin/python3

# -*- coding: utf-8 -*-

import time, threading, random

class ResourseTrand():
    def __init__(self, game_date, maximum_price=100, maximum_deviations=10, k=0.2):
        self.maximum_price = maximum_price
        self.maximum_deviations = maximum_deviations
        self.target = random.randint(1, maximum_price)
        self.current_price = int(self.target/2)
        self.k = k
        self.game_date = game_date

        self.start_demon()
    def demon(self):
        while 1:
            this_day = self.game_date
            self.current_price = (lambda x: int(self.current_price*self.k + (1-self.k)*self.target) if x >=0.8
                                  else int(self.current_price+(self.current_price*self.maximum_deviations)/random.randrange(-100, 100, 200)))(random.random())

            if(abs(self.current_price-self.target)/self.target < 0.05):
                self.target = random.randint(0, maximum_price)
                self.k = self.k + ((random.random()-0.5)/10)
                if(abs(self.k) > 0.8): self.k = 0.5
            while(self.game_date == this_day): pass
    def start_demon(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()
    def getTrand(self):
        return self.current_price
    def SetGameDate(self, date):
        self.game_date = date

