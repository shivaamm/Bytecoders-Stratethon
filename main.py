import numpy as np
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from twilio.rest import Client
from datetime import datetime
import pytz
import threading
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

account_sid = 'AC86129d7f26adf184f62f21db6c4eb8b1'   #Replace with your account_sid'
auth_token = '7dc394031a14f4a084695598a8f90a8b'    #Replace with your auth_token'
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
        hr = int(data['time1'].split(":")[0])
        mn = int(data['time1'].split(":")[1])
        t = lambda: callmsg(data)
        sched.add_job(t, 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()
    if data['time2']:
        sched = BackgroundScheduler()
        print("Afternoon")
        hr = int(data['time2'].split(":")[0])
        mn = int(data['time2'].split(":")[1])
        t1 = lambda: callmsg(data)
        sched.add_job(t1, 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()
    if data['time3']:
        sched = BackgroundScheduler()
        print("Evening")
        hr = int(data['time3'].split(":")[0])
        mn = int(data['time3'].split(":")[1])
        t2 = lambda: callmsg(data)
        sched.add_job(t2, 'cron', day_of_week='mon-sun', hour=hr, minute=mn, timezone=ist)
        sched.start()

def callforRem(data):
    tosay = '<Response><Say>Hi '+data['name']+'. This is a scheduled call from Medcall to remind you to buy '+data['medname']+'. Make sure you get it, thank you.</Say></Response>'
    call = client.calls.create(
          from_='+18507530637',     #Replace with the phone number that you got from Twilio
          twiml=tosay,
          to=data['Phno']   #Phone number that you add on Twilio
    )
    print(call.sid)

def scheduleReminder(data):
    sched = BackgroundScheduler()
    hr = int(data['time'].split(":")[0])
    mn = int(data['time'].split(":")[1])

    yr = int(data['date'].split("-")[0])
    m = int(data['date'].split("-")[1])
    dt = int(data['date'].split("-")[2])
    t = lambda: callforRem(data)
    sched.add_job(t, 'date', run_date=datetime(yr, m, dt, hr, mn, 0), timezone=ist)
    sched.start()
    

app = Flask(__name__)
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
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
        data['Phno'] = "+91"+(request.form.get("Phno"))
        data['time1'] = request.form.get("time1")
        data['time2'] = request.form.get("time2")
        data['time3'] = request.form.get("time3")
        threading.Timer(5.0, scheduleCall(data)).start()
        redirect("https://med-call.herokuapp.com/")
    return render_template('form.html')

@app.route('/medicinereminder', methods =["GET", "POST"])
def medicinereminder():
    if request.method == "POST":
        data = {}
        data['name'] = request.form.get("name")
        data['medname'] = request.form.get("medname")
        data['Phno'] = "+91"+(request.form.get("Phno"))
        data['date'] = request.form.get("date")
        data['time'] = request.form.get("time")
        print(data)
        threading.Timer(5.0, scheduleReminder(data)).start()
        redirect("https://med-call.herokuapp.com/")
    return render_template("medicine-reminder.html") 

@app.route('/appointment')
def appointment():
    return render_template("appointment.html")  

     

if __name__ == '_main_':
    app.run()