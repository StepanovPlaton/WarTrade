#! /usr/bin/python3

# -*- coding: utf-8 -*-

import threading, datetime

from Log import *

class TradeRequestPlayersListClass(DataBaseAPI):
    def __init__(self, ip="192.168.32.10"):
        super().__init__()
        self.Date = "" 
        self.Start()
    def GetList(self, reverse=True): return self.GetTradeRequestPlayersList(reverse)
    def GetTradeRequestPlayersList(self, reverse=True):
        return_value = self.Execute("""SELECT id, date, name, type, resource, quantity, price 
                                 FROM TradeRequestPlayersList ORDER BY id desc;""")
        return (lambda x: return_value[::-1] if(x) else return_value)(reverse)

    def AppendToList(self, name, type_, resource, quantity, price): 
        self.AppendToTradeRequestPlayersList(name, type_, resource, quantity, price)
    def AppendToTradeRequestPlayersList(self, name, type_, resource, quantity, price):
        self.Execute("""INSERT INTO TradeRequestPlayersList(date, name, type, resource, quantity, price)
                        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"""
                        .format(self.Date, name, type_, resource, quantity, int(price)))

    def GetLine(self, id): return self.GetLineInTradeRequestPlayersList(id)
    def GetLineInTradeRequestPlayersList(self, id):
        return self.Execute("""SELECT id, date, name, type, resource, quantity, price 
                                 FROM TradeRequestPlayersList WHERE id={0}""".format(int(id)))

    def DeleteLine(self, id): self.DeleteLineInTradeRequestPlayersList(id)
    def DeleteLineInTradeRequestPlayersList(self, id):
        self.Execute("""DELETE FROM TradeRequestPlayersList WHERE id={0}""".format(id))


    def demon(self):
        while 1:
            self.this_day = self.Date
            while(self.this_day == self.Date): pass
            self.Date_tmp = self.Date.split(".")
            self.Execute("""DELETE FROM TradeRequestPlayersList WHERE date='{0}';"""
                            .format((datetime.datetime(int(self.Date_tmp[2]), int(self.Date_tmp[1]), int(self.Date_tmp[0])) - 
                                    datetime.timedelta(days=3)).strftime("%d.%m.%Y")))
    def Start(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()

    def setGameDate(self, date):
        self.Date = date
