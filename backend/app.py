from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS
import datetime
import serial

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://balisudhir1552005_db_user:12345@cluster0.gy0d1dh.mongodb.net/?appName=Cluster0")
db = client["smart_waste"]
collection = db["sensor_data"]

# GSM Serial Port
# gsm = serial.Serial("COM3",9600,timeout=1)


# Homepage
@app.route('/')
def home():
    return render_template("index.html")


# Receive data from ESP32
@app.route('/update', methods=['POST'])
def update_data():

    data = request.json

    record = {

        "bin1": data.get("bin1"),
        "bin2": data.get("bin2"),
        "bin3": data.get("bin3"),
        "gas": data.get("gas"),
        "level": data.get("level"),
        "type": data.get("type"),
        "time": datetime.datetime.now()

    }

    collection.insert_one(record)

    return jsonify({"status":"stored"})


# Send latest data to webpage
@app.route('/data')
def get_data():

    latest = collection.find().sort("_id",-1).limit(1)

    for d in latest:

        return jsonify({

            "bin1": d["bin1"],
            "bin2": d["bin2"],
            "bin3": d["bin3"],
            "gas": d["gas"],
            "level": d["level"],
            "type": d["type"]

        })

    return jsonify({
        "bin1":0,
        "bin2":0,
        "bin3":0,
        "gas":0,
        "level":0,
        "type":"Normal"
    })


# # GSM SMS
# def send_sms(message):

#     gsm.write(b'AT+CMGF=1\r')
#     gsm.write(b'AT+CMGS="+91XXXXXXXXXX"\r')
#     gsm.write(message.encode())
#     gsm.write(bytes([26]))


# # GSM Call
# def make_call():

#     gsm.write(b'ATD+91XXXXXXXXXX;\r')


# Complaint SMS route
@app.route('/sms')
def sms():

    bin_name = request.args.get("bin")

    msg = "Complaint from Smart Waste System: " + str(bin_name)

    send_sms(msg)

    return "SMS Sent"


# Complaint Call route
@app.route('/call')
def call():

    make_call()

    return "Calling Authority"


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5000)