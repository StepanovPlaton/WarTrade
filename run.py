#! /usr/bin/python3

# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request, jsonify
import os, subprocess, time, threading, subprocess
import requests, logging, random
import matplotlib as mpl
import matplotlib.pyplot as plt

from GraphsForResourceToPNG import *
from GameTimeDemon import *
#from ResourseTrand import *

app = Flask(__name__, template_folder="templates")

app_log = logging.getLogger('werkzeug')
file_handler = logging.FileHandler('log/flask.log', 'w')
app_log.addHandler(file_handler)
app_log.setLevel(logging.INFO)

class ResourseTrand():
    def __init__(self, maximum_price=100, maximum_deviations=10, k=0.5):
        self.maximum_price = maximum_price
        self.maximum_deviations = maximum_deviations
        self.target = random.randint(0, maximum_price)
        self.current_price = int(self.target/2)
        self.k = k
        self.start_demon()
    def demon(self):
        while 1:
            this_day = GameTime.GameDate()
            self.current_price = (lambda x: int(self.current_price*self.k + (1-self.k)*self.target) if x >=0.8
                                  else int(self.current_price+(self.current_price*self.maximum_deviations)/random.randrange(-100, 100, 200)))(random.random())
            if(abs(self.current_price-self.target)/self.target < 0.05):
                self.target = random.randint(0, maximum_price)
                self.k = self.k + ((random.random()-0.5)/10)
                if(abs(self.k) > 0.8): self.k = 0.5
            while(GameTime.GameDate() == this_day): pass
    def start_demon(self):
        demon = threading.Thread(target=self.demon)
        demon.daemon = True
        demon.start()
    def getTrand(self):
        return self.current_price


GameTime = GameTimeServerClass(k=1024)
Graphs = GraphsClass(10)

Money = ResourseTrand()
Wood = ResourseTrand()
Rock = ResourseTrand()

print(str(GameTime.GameTime()))

@app.route("/")
def index(): return render_template("index.html")
@app.route("/middle.html")
def middle(): return render_template("middle.html")
@app.route("/left.html")
def left(): return render_template("left.html")
@app.route("/right.html")
def right(): return render_template("right.html")

@app.route("/get_market", methods=["POST"])
def get_market():
    money = Money.getTrand()
    wood = Wood.getTrand()
    rock = Rock.getTrand()

    Graphs.new_element(money, wood, rock, GameTime.GameDateMini())

    print("MONEY:{0}, WOOD:{1}, ROCK:{2}, TIME - {3}, DATE - {4}".format(money, wood, rock, GameTime.GameTime(), GameTime.GameDate()))

    return jsonify({"money": str(money),
                    "wood": str(wood),
                    "rock": str(rock)})

@app.route("/get_graph", methods=["POST"])
def new_graph(): return jsonify({"graph": str(Graphs.save_new_graphs())})

@app.route("/get_gametime", methods=["POST"])
def get_gametime(): return jsonify({"gametime": GameTime.GameDateTime()})

app.run(host='0.0.0.0', port=5001, debug=False)

