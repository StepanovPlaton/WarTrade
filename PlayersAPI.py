#! /usr/bin/python3

# -*- coding: utf-8 -*-

import random, threading

class Player():
    def __init__(self, name, password, address):
        self.name = name
        self.password = password
        self.online = True
        self.ip = [address]

        self.Money = 300 + random.randint(0, 50)
        self.Gold = 3 + random.randint(0, 5)
        self.Wood = 3 + random.randint(0, 5)
        self.Rock = 3 + random.randint(0, 5)
    def getQuantityResource(self): return (self.Money, self.Wood, self.Rock)

class PlayersClass():
    def __init__(self, LifeTax=10, *Players): 
        self.Players = [i for i in Players]
        self.Date = ""
        self.LifeTax = LifeTax

        self.Start()
    def append(self, Player): self.Players.append(Player)
    def __str__(self):
        out = ""
        for i in self.Players: out+="{0}:{1}:{2} - {3}\n".format(i.ip, i.name, i.password, i.online)
        return out
    def UpdateIP(self, Player):
         if(self.name == Player.name and self.password == Player.password and len(list(set(i.ip + Player.ip))) != 0): self.ip.append(Player.ip)
    def CheckUserUniquenessName(self, Player):
        for i in self.Players:
            if(i.name == Player.name): return False
        return True
    def PasswordValidation(self, Player): return self.getPlayerForName(Player.name).password == Player.password
    def getPlayerForName(self, Name):
        for i in self.Players:
            if(i.name == Name): return i
        return None
    def getIdPlayerForName(self, Name):
        for i in range(len(self.Players)):
            if(self.Players[i].name == Name): return i
        return None

    def TradingWithMarket(self, Name, TypeTransaction, TypeResource, Quantity, Price):
        self.id = self.getIdPlayerForName(Name)
        if(TypeTransaction == "Buy" or TypeTransaction == 0):
            if(TypeResource == "Gold" or TypeResource == 0):
                self.Players[self.id].Money -= Quantity*Price
                self.Players[self.id].Gold += Quantity
            elif(TypeResource == "Wood" or TypeResource == 1):
                self.Players[self.id].Money -= Quantity*Price
                self.Players[self.id].Wood += Quantity
            elif(TypeResource == "Rock" or TypeResource == 2):
                self.Players[self.id].Money -= Quantity*Price
                self.Players[self.id].Rock += Quantity
        elif(TypeTransaction == "Sale" or TypeTransaction == 1):
            if(TypeResource == "Gold" or TypeResource == 0):
                self.Players[self.id].Money += Quantity*Price
                self.Players[self.id].Gold -= Quantity
            elif(TypeResource == "Wood" or TypeResource == 1):
                self.Players[self.id].Money += Quantity*Price
                self.Players[self.id].Wood -= Quantity
            elif(TypeResource == "Rock" or TypeResource == 2):
                self.Players[self.id].Money += Quantity*Price
                self.Players[self.id].Rock -= Quantity

    def demon(self):
        while 1:
            self.this_day = self.Date
            while(self.this_day == self.Date): pass
            for i in self.Players:
                i.Money -= self.LifeTax

    def Start(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()

    def setGameDate(self, date):
        self.Date = date
