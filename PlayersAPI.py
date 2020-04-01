#! /usr/bin/python3

# -*- coding: utf-8 -*-

import random, threading, MySQLdb, time

from DataBaseAPIandLog import *

class Player():
    def __init__(self, sid, name, password, address, Online="Online", 
                Money=450 + random.randint(0, 100), 
                Gold=3 + random.randint(0, 5), 
                Wood=3 + random.randint(0, 5), 
                Rock=3 + random.randint(0, 5)):
        self.sid = sid
        self.name = name
        self.password = password
        self.online = Online
        self.time_apdate = time.time()
        self.ip = address
        self.changed = False

        self.Money = Money
        self.Gold = Gold
        self.Wood = Wood
        self.Rock = Rock

    def getChanged(self): return self.changed
    def setChanged(self, in_): self.changed = in_

    def getQuantityResource(self): return (self.Money, self.Wood, self.Rock)

    def __str__(self):
        return "{0}:{1}:{2}:{3}:{4} - Money={5} Gold={6} Wood={7} Rock={8}\n".format(self.name, self.sid, self.password, self.ip, self.online, 
                                                                                self.Money, self.Gold, self.Wood, self.Rock)

class PlayersClass(DataBaseAPI):
    def __init__(self, LifeTax=10, clear_users_table=False, clear_log_table=False, *Players): 
        super().__init__()
        if(clear_log_table): self.ClearLogTable()
        self.Players = [i for i in Players]
        self.LifeTax = LifeTax

        self.base = MySQLdb.connect("192.168.32.10","platon","maker","WarTrade", use_unicode=True, charset="utf8")
        self.cursor = self.base.cursor()

        if(not clear_users_table):
            self.cursor.execute("SELECT sid, name, password, ip, online, money, gold, wood, rock FROM Players")
            for i in range(self.cursor.rowcount):
                self.line = self.cursor.fetchone()
                self.Players.append(Player(sid=self.line[0], name=self.line[1], password=self.line[2], address=self.line[3], 
                                            Online=self.line[4], Money=int(self.line[5]), Gold=int(self.line[6]),
                                             Wood=int(self.line[7]), Rock=int(self.line[8])))
        else:
            self.cursor.execute("TRUNCATE TABLE Players")

        print((lambda x: "\nИз базы данных были подчитанны следующие пользователи:\n"+self.__str__() 
                if(x>0 and not clear_users_table) 
                else ("\nВ базе данных не было обнаруженно пользователей\n" if(x==0 and not clear_users_table)
                else "\nТаблица пользователей была очищенна в соответсвии с параметром запуска!\n"))(len(self.Players)))

    def append(self, Player): 
        self.LogWrite("К игре присоеденился новый игрок - {}".format(Player.name), color="blue")
        self.appendUserToDatabase(Player)
        self.Players.append(Player)

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

    def getPlayerForSId(self, sid):
        for i in self.Players:
            if(i.sid == sid): return i
        return None
    def getIdPlayerForSId(self, sid):
        for i in range(len(self.Players)):
            if(self.Players[i].sid == sid): return i
        return None

    def getStatusAllPlayers(self, online_only=True):
        returnStatus = []
        for i in self.Players:
            if(online_only):
                if(i.online == "Online"):
                    returnStatus.append([i.name, i.Money, i.Gold, i.Wood, i.Rock])
            else: returnStatus.append([i.name, i.Money, i.Gold, i.Wood, i.Rock]) 
        return returnStatus

    def appendUserToDatabase(self, Player):
        self.Execute("""INSERT INTO Players(name, sid, password, ip, online, money, gold, wood, rock)
                        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')"""
                        .format(Player.name, Player.sid, Player.password, Player.ip, Player.online, 
                                str(Player.Money), str(Player.Gold), str(Player.Wood), str(Player.Rock)))

    def updateDatabase(self, Name):
        self.Player = self.getPlayerForName(Name)
        self.setActive(Name)
        self.Execute("""UPDATE Players SET ip='{3}', online='{4}', money='{5}', gold='{6}', wood='{7}', rock='{8}' WHERE NAME='{0}' AND PASSWORD='{1}' AND SID='{2}';"""
                    .format(self.Player.name, self.Player.sid, self.Player.password, self.Player.ip, self.Player.online, str(self.Player.Money), str(self.Player.Gold), str(self.Player.Wood), str(self.Player.Rock)))
        
        self.id = self.getIdPlayerForName(Name)
        self.Players[self.id].setChanged(True)

    def setActive(self, Name):
        self.Players[self.getIdPlayerForName(Name)].time_apdate = time.time()

    def __str__(self):
        for i in self.Players:
            return str(i)

    def TradingWithMarket(self, Name, TypeTransaction, TypeResource, Quantity, Price):
        self.id = self.getIdPlayerForName(Name)
        self.Players[self.id].time_apdate = time.time()

        self.out = False

        if(TypeTransaction == "Buy" or TypeTransaction == 0):
            if(self.Players[self.id].Money >= Quantity*Price):
                if(TypeResource == "Gold" or TypeResource == 0):
                    self.Players[self.id].Money -= Quantity*Price
                    self.Players[self.id].Gold += Quantity
                    self.out = True
                elif(TypeResource == "Wood" or TypeResource == 1):
                    self.Players[self.id].Money -= Quantity*Price
                    self.Players[self.id].Wood += Quantity
                    self.out = True
                elif(TypeResource == "Rock" or TypeResource == 2):
                    self.Players[self.id].Money -= Quantity*Price
                    self.Players[self.id].Rock += Quantity
                    self.out = True
        elif(TypeTransaction == "Sale" or TypeTransaction == 1):
            if(TypeResource == "Gold" or TypeResource == 0):
                if(self.Players[self.id].Gold >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Gold -= Quantity
                    self.out = True
            elif(TypeResource == "Wood" or TypeResource == 1):
                if(self.Players[self.id].Wood >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Wood -= Quantity
                    self.out = True
            elif(TypeResource == "Rock" or TypeResource == 2):
                if(self.Players[self.id].Rock >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Rock -= Quantity
                    self.out = True
        self.LogWrite("Игрок {0} {1} {2} в количестве {3}шт. по цене в {4} монет"
                        .format(self.Players[self.id].name, (lambda x: "купил" if(x==0) else "продал")(TypeTransaction), 
                                (lambda x: "золото" if(x==0) else ("дерево" if(x==1) else "камень"))(TypeResource),
                                Quantity, Price),
                        type_message="game", look="FALSE")
        self.updateDatabase(Name)

        return self.out

    def setGameDate(self):
        for i in self.Players:
            if((time.time() - i.time_apdate) < 15):
                if(i.online != "Online"):
                    i.Money -= self.LifeTax
            self.updateDatabase(i.name)
        return self.getStatusAllPlayers()
