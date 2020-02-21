#! /usr/bin/python3

# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request, jsonify
import os, subprocess, time, threading, subprocess
import requests, logging, random
import matplotlib as mpl
import matplotlib.pyplot as plt

from GraphsForResourceToPNG import *
from GameTimeDemon import *
from ResourseTrand import *
from PlayersAPI import *

app = Flask(__name__, template_folder="templates")

app_log = logging.getLogger('werkzeug')
file_handler = logging.FileHandler('log/flask.log', 'w')
app_log.addHandler(file_handler)
app_log.setLevel(logging.INFO)

def GameTimeTransfer():
    while 1:
        Money.SetGameDate(GameTime.GameDate())
        Wood.SetGameDate(GameTime.GameDate())
        Rock.SetGameDate(GameTime.GameDate())

GameTime = GameTimeServerClass(k=1024)
Graphs = GraphsClass(10)

Money = ResourseTrand(GameTime.GameDate())
Wood = ResourseTrand(GameTime.GameDate())
Rock = ResourseTrand(GameTime.GameDate())

Players = PlayersClass()

demon = threading.Thread(target=GameTimeTransfer)
demon.daemon = True
demon.start()

@app.route("/")
def welcome(): return render_template("welcome.html")

@app.route("/start.html")
def start():
    GameTime.Start()
    return render_template("index.html")

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
    Graphs.NewElement(money, wood, rock, GameTime.GameDateMini(), GameTime.GameDate())
    print("MONEY:{0}, WOOD:{1}, ROCK:{2}, TIME - {3}, DATE - {4}".format(money, wood, rock, GameTime.GameTime(), GameTime.GameDate()))
    return jsonify({"money": str(money), "wood": str(wood), "rock": str(rock)})

@app.route("/get_graph", methods=["POST"])
def new_graph(): return jsonify({"graph": str(Graphs.GetActualGraph())})
@app.route("/get_gametime", methods=["POST"])
def get_gametime(): return jsonify({"gametime": GameTime.GameDateTime()})

@app.route("/login", methods=["POST"])
def Login():
    login = request.form.get("login")
    password = request.form.get("password")
    LoginPlayer = Player(login, password, request.remote_addr)
    LoginUserWithUniqueName = Players.CheckUserUniquenessName(LoginPlayer)

    if(LoginUserWithUniqueName):
        Players.append(LoginPlayer)
        print(Players)
        return jsonify({"answer": "LOGINOK"})
    elif(not LoginUserWithUniqueName):
        LoginUserWithValidationPassword = Players.PasswordValidation(LoginPlayer)
        if(not LoginUserWithValidationPassword): return jsonify({"answer": open('SystemMessages/NameBusy.txt').read()})
        else: return jsonify({"answer": "LOGINOK"})

app.run(host='0.0.0.0', port=5001, debug=False)

