from flask import Flask, render_template, send_from_directory
from flask_restful import Api, Resource, reqparse, abort
import pickle
import os

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
    return render_template("live.html")

@app.route('/stats')
def stats():
    return render_template("statistics.html")


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html") 



class WeatherPred(Resource):

    def get(self, num):
        return {"Api": "Is Working", "number" : num}

api.add_resource(WeatherPred, "/api/<int:num>")