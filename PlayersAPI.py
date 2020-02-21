#! /usr/bin/python3

# -*- coding: utf-8 -*-

class Player():
    def __init__(self, name, password, address):
        self.name = name
        self.password = password
        self.online = True
        self.ip = [address]

class PlayersClass():
    def __init__(self, *Players): self.Players = [i for i in Players]
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
    def PasswordValidation(self, Player): return self.GetPlayerForName(Player.name).password == Player.password
    def GetPlayerForName(self, Name):
        for i in self.Players:
            if(i.name == Name): return i
        return None
