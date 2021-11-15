import numpy as np
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from twilio.rest import Client
from datetime import datetime
import pytz
import threading
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

account_sid = 'AC86129d7f26adf184f62f21db6c4eb8b1'   #Replace with your account_sid'
auth_token = 'd8a01efe784c1f30e4d6633a97d04b14'    #Replace with your auth_token'
client = Client(account_sid, auth_token)
ist = pytz.timezone('Asia/Kolkata')

def callmsg(data):   
    whatsappNo = 'whatsapp:'+data['Phno']
    tosay = '<Response><Say>Hi '+data['Name']+'. This is a scheduled call from Medcall to remind you to take '+data['Medicine']+'. Thank you.</Say></Response>'
    call = client.calls.create(
          from_='+18507530637',     #Replace with the phone number that you got from Twilio
          twiml=tosay,
          to=data['Phno']   #Phone number that you add on Twilio
    )
    message = client.messages.create(
         body='Reminder from Medcall for ' +data['Name']+' . Please take '+data['Medicine']+'. Thank you.',
         from_='whatsapp:+14155238886',
         to=whatsappNo
     )
    print(call.sid)
    print(message.sid)
def scheduleCall(data):
    if data['time1']:
        sched = BackgroundScheduler()
        print("Morning")
        hr = int(data['time1'].split(":")[0])
        mn = int(data['time1'].split(":")[1])
        sched.add_job(lambda: callmsg(data), 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()
        # job1.remove()
        # sched.shutdown()
    if data['time2']:
        sched = BackgroundScheduler()
        print("Afternoon")
        hr = int(data['time2'].split(":")[0])
        mn = int(data['time2'].split(":")[1])
        sched.add_job(lambda: callmsg(data), 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()
    if data['time3']:
        sched = BackgroundScheduler()
        print("Evening")
        hr = int(data['time3'].split(":")[0])
        mn = int(data['time3'].split(":")[1])
        sched.add_job(lambda: callmsg(data), 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()
    
app = Flask(__name__)
@app.route('/')
def home_page():
    return redirect(url_for('welcome'))
@app.route('/welcome')
def welcome():
    return render_template("index.html")
@app.route("/start")
def start():
    return redirect(url_for('welcome'))
@app.route('/form', methods =["GET", "POST"])
def formData():
    if request.method == "POST":
        data = {}
        data['Name'] = request.form.get("Name")
        data['Medicine'] = request.form.get("Medicine")
        data['Phno'] = "+91"+str(request.form.get("Phno"))
        data['time1'] = request.form.get("time1")
        data['time2'] = request.form.get("time2")
        data['time3'] = request.form.get("time3")
        threading.Timer(5.0, scheduleCall(data)).start()
        # while True:
        #     scheduleCall(data)
        # return jsonify(data)
    return render_template('form.html')
if __name__ == '__main__':
    app.run()