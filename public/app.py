from flask import Flask, render_template, send_from_directory
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
    return render_template("live.html", a = a)

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

        d= {"windspeed": windspeed, "humidity": humidity, "temp":temp}


        return d

api.add_resource(WeatherPred, "/api/<con>")