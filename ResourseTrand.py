#! /usr/bin/python3

# -*- coding: utf-8 -*-

import time, threading, random

class ResourseTrand():
    def __init__(self, game_date, maximum_price=100, maximum_deviations=10, rate_change=50):
        self.maximum_price = maximum_price
        self.maximum_deviations = maximum_deviations
        self.target = random.randint(1, maximum_price)
        self.current_price = int(self.target/2)
        self.rate_change = rate_change
    
    def getTrand(self): return self.current_price

    def getNewTrand(self):
        self.r = random.random() * 4
        self.current_price = int((self.current_price + (self.target - self.current_price)/
                             (self.rate_change/2 + (random.random() * self.rate_change)/2)) + random.random() * self.r/2 - self.r)
        
        if(self.current_price > self.maximum_price): 
            self.current_price = self.maximum_price - random.randint(0, 5) 
        elif(self.current_price < 1): 
            self.current_price = 0 + random.randint(0, 5) 
        
        if(abs(self.current_price-self.target)/self.target < 0.1):
            self.target = random.randint(1, self.maximum_price)
        return self.current_price
        

