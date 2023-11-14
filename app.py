
from distutils.log import debug
import json
from flask import Flask, jsonify, render_template, request
import time
import diseaseprocess 
import medicineprocess 
import symtomedprocess
import nameprocess
from flask_ngrok import run_with_ngrok

t = time.localtime()
current_time = time.strftime("%H:%M", t)

app = Flask(__name__)
# run_with_ngrok(app)
menu =["Give medicine for symptoms","Enter Medicine name","Enter symptoms to get disease","Learn about a Disease"]

@app.route("/")
def home():
    return render_template("chatbot.html",menu_options = menu, currentTime = current_time)

@app.route("/res",methods = ["POST"])
def botresponse():
    rawTxt = request.form['msg'] 
    print(rawTxt)
    txt = rawTxt.split(".")
    modelno =txt[0]
    msg = txt[1]
    # cmsg = msg[:4]
    # print(type(modelno))
    # print(len(cmsg))
    # if cmsg == "menu":
        # return jsonify({"response":"Choices resetted", "modelno": 0})
    if (modelno == "1"):
        response = symtomedprocess.chatbot_response(msg)
        return jsonify({"response":response,"modelno": modelno})
    elif (modelno == "2"):
        response = medicineprocess.chatbot_response(msg)
        return jsonify({"response": response, "modelno": modelno})
    elif (modelno == "3"):
        response = diseaseprocess.chatbot_response(msg)
        
        return jsonify({"response": response, "modelno": modelno })
    elif (modelno == "4"):
        response = nameprocess.chatbot_response(msg)
        return jsonify({"response": response, "modelno": modelno })
    else:
        return "Please give valid input"
    # return "model no: "+ modelno + " msg: "+ msg


if __name__ == "__main__":
    app.run(port= '8000',debug = True)
