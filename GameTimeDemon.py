#! /usr/bin/python3

# -*- coding: utf-8 -*-

import time, threading

class GameTimeServerClass():
    def __init__(self, time_start=time.time(), k=16):
        self.time_start=time_start
        self.k = k
        self.game_time = time_start
    def demon(self):
        while 1:
            self.game_time = time.time() + (time.time()-self.time_start)*self.k
            time.sleep(0.5)
    def Start(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()
    def GameDateTime(self):
        return time.strftime("%X %d.%m.%Y", time.gmtime(self.game_time))
    def GameTime(self):
        return time.strftime("%X", time.gmtime(self.game_time))
    def GameDate(self):
        return time.strftime("%d.%m.%Y", time.gmtime(self.game_time))
    def GameDateMini(self):
        return time.strftime("%d.%m", time.gmtime(self.game_time))
