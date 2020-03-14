#! /usr/bin/python3

# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request, jsonify, send_from_directory
import os, subprocess, time, threading, subprocess
import requests, logging, random, sys
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
        Gold.setGameDate(GameTime.GameDate())
        Wood.setGameDate(GameTime.GameDate())
        Rock.setGameDate(GameTime.GameDate())
        Players.setGameDate(GameTime.GameDate())

GameTime = GameTimeServerClass(k=4096)
Graphs = GraphsClass(10)

Gold = ResourseTrand(GameTime.GameDate())
Wood = ResourseTrand(GameTime.GameDate())
Rock = ResourseTrand(GameTime.GameDate())

clear_log = False
clear_users = False

for i in sys.argv:
    if(i.find("--clear_users") != -1 or i.find("-cu") != -1): clear_users = True
    elif(i.find("--clear_log") != -1 or i.find("-cl") != -1): clear_log = True

Players = PlayersClass(10, clear_users, clear_log)

demon = threading.Thread(target=GameTimeTransfer)
demon.daemon = True
demon.start()

@app.route("/")
def welcome(): return render_template("welcome.html")

@app.route("/start.html")
def start():
    return render_template("index.html")

@app.route("/middle.html")
def middle(): return render_template("middle.html")
@app.route("/left.html")
def left(): return render_template("left.html")
@app.route("/right.html")
def right(): return render_template("right.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/get_market_and_table_online_and_gametime", methods=["POST"])
def get_market():
    gold = Gold.getTrand()
    wood = Wood.getTrand()
    rock = Rock.getTrand()
    Graphs.NewElement(gold, wood, rock, GameTime.GameDateMini(), GameTime.GameDate())
    #print("GOLD:{0}, WOOD:{1}, ROCK:{2}, TIME - {3}, DATE - {4}".format(gold, wood, rock, GameTime.GameTime(), GameTime.GameDate()))
    return jsonify({"money": str(gold), "wood": str(wood), "rock": str(rock),
                    "status": Players.getStatusAllPlayers(),
                    "gametime": GameTime.GameDateTime()})

@app.route("/get_graph", methods=["GET"])
def new_graph(): 
    data = Graphs.GetActualGraph()
    return f"data:image/png;base64,{data}"

@app.route("/log", methods=["POST"])
def log(): 
    if(request.form.get("type") == "1" or request.form.get("type") == "send"):
        Players.LogWrite(request.form.get("message"), "message", request.form.get("login"))
    return jsonify({"log": Players.LogRead(10)})

@app.route("/user_status_or_trade", methods=["POST"])
def Trade():
    login = request.form.get("login")
    password = request.form.get("password")
    typeRequest = request.form.get("type")
    RequestPlayer = Players.getPlayerForName(login)

    if(typeRequest == "trade"):
        typeResource = request.form.get("typeResource")
        typeTransaction = request.form.get("typeTransaction")
        Quantity = request.form.get("Quantity")
        if(typeResource == "Gold"): Price = Gold.getTrand()
        elif(typeResource == "Wood"): Price = Wood.getTrand()
        elif(typeResource == "Rock"): Price = Rock.getTrand()

        Players.TradingWithMarket(login, typeTransaction, typeResource, int(Quantity), Price)
    return jsonify({"Money": Players.getPlayerForName(login).Money,
                    "Gold": Players.getPlayerForName(login).Gold,
                    "Wood": Players.getPlayerForName(login).Wood,
                    "Rock": Players.getPlayerForName(login).Rock})

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

