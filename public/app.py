from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_restful import Api, Resource, reqparse, abort
import pickle
import os
import json 
import requests


from public.variables import country, apik


app = Flask(__name__)
api = Api(app)




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/icon.ico')
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/developer")
def dev():
    return render_template("developer.html")

@app.route("/live")
def live():
    a = country.country()
    d = {'windspeed': 0, 'humidity': 0, 'temp':0, 'class': 0}
    return render_template("live.html", a = a, d= d)

@app.route('/live1', methods = ["GET", "POST"])
def live1():
    a = country.country()
    coun  = request.form.get("con")
    print(coun)
    if coun is not None:
        name = coun
    else:
        name = "india"

    print(name)
    url = "https://bppcov19.herokuapp.com/api/"+name
    d = json.loads(requests.get(url).text)
    return render_template("live.html", a = a, d = d)


def redir():
    return redirect(url_for('live'))

@app.route('/stats')
def stats():
    return render_template("statistics.html")


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html") 



class WeatherPred(Resource):

    def get(self, con):
        key = apik.getkey()
        url = "http://api.weatherstack.com/current?access_key="+key+"&query="+con
        r = requests.get(url)

        y = json.loads(r.text)['current']
        windspeed = y['wind_speed']
        humidity = y['humidity']
        temp = y['temperature']
        

        d= {"windspeed": windspeed, "humidity": humidity, "temp":temp, "class": 1}


        return d

api.add_resource(WeatherPred, "/api/<con>")