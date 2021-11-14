import numpy as np
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

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
        filter = {}
        filter['Label'] = request.form.get("label")
        skin = request.form.getlist("skin")
        for x in skin:
            if x == "Combination":
                filter['Combination'] = 1
            if x == "Dry":
                filter['Dry'] = 1
            if x == "Normal":
                filter['Normal'] = 1
            if x == "Oily":
                filter['Oily'] = 1
            if x == "Sensitive":
                filter['Sensitive'] = 1
        price_min = int(request.form['price-min'])
        price_max = int(request.form['price-max'])
        filter['price'] = { "$lte" : price_max, "$gte" : price_min}
        return jsonify(filter)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)