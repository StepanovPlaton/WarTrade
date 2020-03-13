#! /usr/bin/python3

# -*- coding: utf-8 -*-

import random, threading, MySQLdb, time

from Log import *

class Player():
    def __init__(self, name, password, address, Online="Online", Money=450 + random.randint(0, 100), Gold=3 + random.randint(0, 5), 
                Wood=3 + random.randint(0, 5), Rock=3 + random.randint(0, 5)):
        self.name = name
        self.password = password
        self.online = Online
        self.time_apdate = time.time()
        self.ip = address

        self.Money = Money
        self.Gold = Gold
        self.Wood = Wood
        self.Rock = Rock
    def getQuantityResource(self): return (self.Money, self.Wood, self.Rock)

    def __str__(self):
        return "{0}:{1}:{2}:{3} - Money={4} Gold={5} Wood={6} Rock={7}\n".format(self.name, self.password, self.ip,
                                                                                self.online, self.Money, self.Gold,
                                                                                self.Wood, self.Rock)

class PlayersClass(LogClass):
    def __init__(self, LifeTax=10, clear_users_table=False, *Players): 
        super().__init__()
        self.Players = [i for i in Players]
        self.Date = ""
        self.LifeTax = LifeTax

        self.base = MySQLdb.connect("192.168.32.10","platon","maker","WarTrade", use_unicode=True, charset="utf8")
        self.cursor = self.base.cursor()
        self.cursor.execute("SET NAMES 'utf8'")
        self.cursor.execute("SET CHARACTER SET 'utf8'")
        self.cursor.execute("SET SESSION collation_connection = 'utf8_general_ci'")
        self.base.commit()

        if(not clear_users_table):
            self.cursor.execute("SELECT name, password, ip, online, money, gold, wood, rock FROM Players")
            for i in range(self.cursor.rowcount):
                self.line = self.cursor.fetchone()
                self.Players.append(Player(name=self.line[0], password=self.line[1], address=self.line[2], 
                                            Online=self.line[3], Money=int(self.line[4]), Gold=int(self.line[5]),
                                             Wood=int(self.line[6]), Rock=int(self.line[7])))
        else:
            self.cursor.execute("TRUNCATE TABLE Players")

        print((lambda x: "\nИз базы данных были подчитанны следующие пользователи:\n"+self.__str__() 
                if(x>0 and not clear_users_table) 
                else ("\nВ базе данных не было обнаруженно пользователей\n" if(x==0 and not clear_users_table)
                else "\nТаблица пользователей была очищенна в соответсвии с параметром запуска!\n"))(len(self.Players)))
        self.Start()

    def append(self, Player): 
        #self.LogWrite("К игре присоеденился новый игрок - {}".format(Player.name), color="blue")
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

    def getStatusAllPlayers(self):
        returnStatus = []
        for i in self.Players:
            returnStatus.append([i.name, i.Money, i.Gold, i.Wood, i.Rock])
        return returnStatus

    def appendUserToDatabase(self, Player):
        self.cursor.execute("""INSERT INTO Players(name, password, ip, online, money, gold, wood, rock)
                                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')"""
                            .format(Player.name, Player.password, Player.ip, Player.online, 
                                    str(Player.Money), str(Player.Gold), str(Player.Wood), str(Player.Rock)))
        self.base.commit()

    def updateDatabase(self, Name):
        #self.cursor.close() 
        #self.cursor = self.base.cursor() 
        self.Player = self.getPlayerForName(Name)
        self.cursor.execute("""UPDATE Players SET ip='{2}', online='{3}', money='{4}', gold='{5}', wood='{6}', rock='{7}' WHERE NAME='{0}' AND PASSWORD='{1}';"""
            .format(self.Player.name, self.Player.password, self.Player.ip, self.Player.online, str(self.Player.Money), str(self.Player.Gold), str(self.Player.Wood), str(self.Player.Rock)))
        self.base.commit()

    def __str__(self):
        for i in self.Players:
            return str(i)

    def TradingWithMarket(self, Name, TypeTransaction, TypeResource, Quantity, Price):
        self.id = self.getIdPlayerForName(Name)
        self.Players[self.id].time_apdate = time.time()
        if(TypeTransaction == "Buy" or TypeTransaction == 0):
            if(self.Players[self.id].Money >= Quantity*Price):
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
                if(self.Players[self.id].Gold >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Gold -= Quantity
            elif(TypeResource == "Wood" or TypeResource == 1):
                if(self.Players[self.id].Wood >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Wood -= Quantity
            elif(TypeResource == "Rock" or TypeResource == 2):
                if(self.Players[self.id].Rock >= Quantity):
                    self.Players[self.id].Money += Quantity*Price
                    self.Players[self.id].Rock -= Quantity
        self.LogWrite("Игрок {0} {1} {2} в количестве {3}шт. по цене в {4} монет"
                        .format(self.Players[self.id].name, (lambda x: "купил" if(x==0) else "продал")(TypeTransaction), 
                                (lambda x: "золото" if(x==0) else ("дерево" if(x==1) else "камень"))(TypeResource),
                                Quantity, Price),
                        type_message="game", look="FALSE")
        self.updateDatabase(Name)

    def demon(self):
        while 1:
            self.this_day = self.Date
            while(self.this_day == self.Date): pass
            self.LogWrite("Наступил новый день! Сегодня {}".format(self.Date), text_type="blod", type_message="info")
            for i in self.Players:
                if((time.time() - i.time_apdate) < 15):
                    i.online = "Online"
                    i.Money -= self.LifeTax
                    self.LogWrite("В игру вошёл {}".format(i.name), color="green")
                else:
                    i.online = time.strftime("%X %d.%m.%Y", time.gmtime(time.time()))
                self.updateDatabase(i.name)

    def Start(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()

    def setGameDate(self, date):
        self.Date = date
