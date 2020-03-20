#! /usr/bin/python3

# -*- coding: utf-8 -*-

import MySQLdb

class DataBaseAPI():
    def __init__(self, ip="192.168.32.10", len=50):
        self.ip_default = ip
    def LogWrite(self, message, type_message="system", user="system", color="black", text_type="normal", look="TRUE", quiet=False):
        self.Execute("""INSERT INTO Log(message, type, user, color, text_type, look)
                        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"""
                        .format(message, type_message, user, color, text_type, look))
        if(not quiet): 
            print("{0} {1} {2} {3} {4}".format(message, type_message, user, color, text_type))

    def LogRead(self, len=10, admin="FALSE", reverse=True, quiet=False):
        return_value = self.Execute("SELECT message, type, user, color, text_type FROM Log"+
                                    (lambda x: " WHERE look='TRUE'" if(admin=="FALSE") else " ") (type)
                                    + " ORDER BY id desc LIMIT {0};".format(len))
        return (lambda x: return_value[::-1] if(x) else return_value)(reverse)

    def Execute(self, command, quiet=False, ip="default"):
        base = MySQLdb.connect((lambda x: self.ip_default if(x=="default") else ip)(ip),"platon","maker","WarTrade", use_unicode=True, charset="utf8")
        return_value = None
        try:
            cursor = base.cursor()
            cursor.execute(command)
            if(command.lower().find("select") != -1):
                return_value = cursor.fetchall()
            cursor.close()
            base.commit()
        except BaseException as e: 
            if(not quiet): 
                print("! ERROR ! Command -", command)
                print("Transaction failed, rolling back")
            base.rollback()
        return return_value

    def ClearLogTable(self, quiet=False):
        if(not quiet): print("\nТаблица лога была очищенна в соответсвии с параметром запуска!")
        self.Execute("TRUNCATE TABLE Log")

    def __str__(self):
        out = ""
        for i in self.LogRead():
            for j in i: out += j+"   "
            out+="\n"
        return out