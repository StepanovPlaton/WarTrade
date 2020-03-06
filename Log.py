#! /usr/bin/python3

# -*- coding: utf-8 -*-

import MySQLdb

class Log():
    def __init__(self, ip="192.168.32.10"):
        self.base = MySQLdb.connect(ip,"platon","maker","WarTrade", use_unicode=True, charset="utf8")
        self.cursor = self.base.cursor()
    def LogWrite(self, message, type_message="system", user="system", color="black", text_type="normal", look="TRUE", quiet=False):
        self.cursor.execute("""INSERT INTO Log(message, type, user, color, text_type, look)
                                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"""
                                .format(message, type_message, user, color, text_type, look))
        self.base.commit()
        if(not quiet): print("{0} {1} {2} {3} {4}".format(message, type_message, user, color, text_type))

    def LogRead(self, len=10, admin="FALSE"):
        self.cursor.execute("SELECT message, type, color, text_type FROM Log"+
                            (lambda x: " WHERE look='TRUE'" if(admin=="FALSE") else " ") (type)
                            + " ORDER BY id desc LIMIT {0};".format(len))
        return self.cursor.fetchall()

    def __str__(self):
        out = ""
        for i in self.LogRead():
            for j in i: out += j+"   "
            out+="\n"
        return out