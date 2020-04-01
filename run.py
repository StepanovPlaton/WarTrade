#! /usr/bin/python3

# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request, jsonify, send_from_directory
import os, subprocess, time, threading, subprocess
from flask_socketio import SocketIO, send, emit
import requests, logging, random, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from flask_cors import CORS

from GraphsForResourceToPNG import *
from GameTimeDemon import *
from ResourseTrand import *
from PlayersAPI import *
from TradeRequestPlayersListClass import *
from DataBaseAPIandLog import *

app = Flask(__name__, template_folder="templates")
CORS(app)
sio = SocketIO(app)

app_log = logging.getLogger('werkzeug')
file_handler = logging.FileHandler('log/flask.log', 'w')
app_log.addHandler(file_handler)
app_log.setLevel(logging.INFO)

def DailyCycleUpdates():
    while 1:
        today = GameTime.GameDate()
        while(today == GameTime.GameDate()): time.sleep(0.1)
        TradeRequestPlayersList.setGameDate(GameTime.GameDate())
        status = Players.setGameDate()

        gold = Gold.getNewTrand()
        wood = Wood.getNewTrand()
        rock = Rock.getNewTrand()
        Graph = Graphs.NewElement(gold, wood, rock, GameTime.GameDateMini())

        with app.test_request_context('/'):
            sio.emit("market_and_table_online_and_gametime", 
                    {"money": str(gold), "wood": str(wood), "rock": str(rock),
                    "status": status,
                    "gametime": GameTime.GameDate(),
                    "graph": f"data:image/png;base64,{Graph}"},
                    broadcast=True)
        time.sleep(1)

def SituationalUpdates():
    while 1:
        if(Log.getChanged()):
            with app.test_request_context('/'):
                sio.emit("get_log", {"log": Log.LogRead(10)}, broadcast=True)
            Log.setChanged(False)
        if(TradeRequestPlayersList.getChanged()):
            with app.test_request_context('/'):
                sio.emit("trade_players_list", {"tradeplayerlist": TradeRequestPlayersList.GetList()}, broadcast=True)
            TradeRequestPlayersList.setChanged(False)
        for i in Players.Players:
            if(i.getChanged()):
                with app.test_request_context('/'):
                    emit("status_player", {
                            "Money": i.Money,
                            "Gold": i.Gold,
                            "Wood": i.Wood,
                            "Rock": i.Rock}, 
                            room=i.sid, namespace='/')
                    #print(i.name, "SEND STATUS")
                i.setChanged(False)

        time.sleep(1)

TradeRequestPlayersList = TradeRequestPlayersListClass()

GameTime = GameTimeServerClass(k=4096)
Graphs = GraphsClass(10)

Gold = ResourseTrand(GameTime.GameDate())
Wood = ResourseTrand(GameTime.GameDate())
Rock = ResourseTrand(GameTime.GameDate())

Log = DataBaseAPI()

clear_log = False
clear_users = False

for i in sys.argv:
    if(i.find("--clear_users") != -1 or i.find("-cu") != -1): clear_users = True
    elif(i.find("--clear_log") != -1 or i.find("-cl") != -1): clear_log = True

Players = PlayersClass(10, clear_users, clear_log)

demon = threading.Thread(target=DailyCycleUpdates)
demon.daemon = True
demon.start()
demon2 = threading.Thread(target=SituationalUpdates)
demon2.daemon = True
demon2.start()

@sio.on('send_sid')
def send_sid(name):
    id_sid = Players.getIdPlayerForName(name)
    Players.Players[id_sid].sid = request.sid
    print("{} Зашёл в игру".format(name))
    Log.LogWrite("В игру вошёл {}".format(name), color="green")
    Players.Players[id_sid].online = "Online"

@sio.on('disconnect')
def disconnect():
    try:
        id_sid = Players.getIdPlayerForSId(request.sid)
        print("{0} Вышел из игры".format(Players.Players[id_sid].name))
        Log.LogWrite("Из игры вышел {}".format(name), color="green")
        Players.Players[id_sid].online = time.strftime("%X %d.%m.%Y", time.gmtime(time.time()))
    except BaseException: pass
    
@app.route("/")
def index(): return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/send_to_log", methods=["POST"])
def send_to_log(): 
    Log.LogWrite(request.form.get("message"), "message", request.form.get("login"))
    return jsonify({})

@app.route("/get_tradeplayerlist", methods=["POST"])
def get_tradeplayerlist():

    if(request.form.get("type") == "approv"):
        TradeRequest = (TradeRequestPlayersList.GetLine(request.form.get("id")))[0]
        Player1 = Players.getIdPlayerForName(TradeRequest[2])
        Player2 = Players.getIdPlayerForName(request.form.get("login"))

        if(TradeRequest[3] == "Sale"):
            Player_tmp = Player1
            Player1 = Player2
            Player2 = Player_tmp

        result = False

        Players.Players[Player2].Money += int(TradeRequest[6])*int(TradeRequest[5])
        Players.Players[Player1].Money -= int(TradeRequest[6])*int(TradeRequest[5])
        if(TradeRequest[4] == "Gold" and Players.Players[Player2].Gold >= TradeRequest[5]):
            Players.Players[Player2].Gold -= TradeRequest[5]
            Players.Players[Player1].Gold += TradeRequest[5]
            result = True
        elif(TradeRequest[4] == "Wood" and Players.Players[Player2].Wood >= TradeRequest[5]):
            Players.Players[Player2].Wood -= TradeRequest[5]
            Players.Players[Player1].Wood += TradeRequest[5]
            result = True
        elif(TradeRequest[4] == "Rock" and Players.Players[Player2].Rock >= TradeRequest[5]):
            Players.Players[Player2].Rock -= TradeRequest[5]
            Players.Players[Player1].Rock += TradeRequest[5]
            result = True

        if(result):
            TradeRequestPlayersList.DeleteLine(TradeRequest[0])
            Log.LogWrite("Игрок {0} и игрок {1} заключили сделку на {2} монет"
                        .format(Players.Players[Player1].name, Players.Players[Player2].name, TradeRequest[6]), "game")
    elif(request.form.get("type") == "close"):
        TradeRequestPlayersList.DeleteLine(request.form.get("id"))
        Log.LogWrite("Игрок {0} отменил cвоё предложение"
                    .format(request.form.get("login")), "game")
    return jsonify({})

@app.route("/user_status_or_trade", methods=["POST"])
def Trade():
    login = request.form.get("login")
    password = request.form.get("password")
    typeRequest = request.form.get("type")
    RequestPlayer = Players.getPlayerForName(login)

    Players.setActive(login)
    
    typeResource = request.form.get("typeResource")
    typeTransaction = request.form.get("typeTransaction")
    Quantity = request.form.get("Quantity")
    
    if(typeRequest == "trade with market"):
        if(typeResource == "Gold"): Price = Gold.getTrand()
        elif(typeResource == "Wood"): Price = Wood.getTrand()
        elif(typeResource == "Rock"): Price = Rock.getTrand()
        Players.TradingWithMarket(login, typeTransaction, typeResource, int(Quantity), Price)
    elif(typeRequest == "trade with players"):
        Price = request.form.get("Price")
        TradeRequestPlayersList.AppendToList(login, typeTransaction, typeResource, int(Quantity), int(Price))
        Log.LogWrite("Игрок {0} выложил заявку на {1} монет"
                    .format(request.form.get("login"), Price), "game")
    return jsonify({})

@app.route("/login", methods=["POST"])
def Login():
    login = request.form.get("login")
    password = request.form.get("password")
    LoginPlayer = Player(None, login, password, request.remote_addr)
    LoginUserWithUniqueName = Players.CheckUserUniquenessName(LoginPlayer)

    if(LoginUserWithUniqueName):
        Players.append(LoginPlayer)
        print(Players)
        return jsonify({"answer": "LOGINOK"})
    elif(not LoginUserWithUniqueName):
        LoginUserWithValidationPassword = Players.PasswordValidation(LoginPlayer)
        if(not LoginUserWithValidationPassword): return jsonify({"answer": open('SystemMessages/NameBusy.txt').read()})
        else: return jsonify({"answer": "LOGINOK"})


sio.run(app, host="0.0.0.0", port=5001)
#app.run(host='0.0.0.0', port=5001, debug=False)

