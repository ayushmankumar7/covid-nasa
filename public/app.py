from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_restful import Api, Resource, reqparse, abort
import pickle
import os
import json 
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output



from public.variables import country, apik


external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]
data=pd.read_csv('public/facccc.csv')

options=[{'label':'confirmed','value':'confirmed'},
          {'label':'deaths','value':'deaths'}
          ]
options2=[{'label':'0-2000','value':'0-2000'},
          {'label':'2001-3000','value':'2001-3000'},
          {'label':'3001-80000','value':'3001-80000'},
          {'label':'80000+','value':'80000+'}

          ]







app = Flask(__name__)
api = Api(app)
dhpp = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=app, url_base_pathname= '/pathname/')
model = pickle.load(open('public/model/model.pkl', 'rb'))
print(model)


dhpp.layout=html.Div([
    html.H1("Corona Virus Pandemic",style={'color':'#fff','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4("The Graphs given below are there to show how the various enviromental factors affect the covid cases.In order to understand the visualization we need to select the criterion for the number of covid cases from the dropdown ,accordingly a box plot with frequency distribution will be shown.Thus by considering this we can understand the median and interquartile ranges of the particular enviromental factor for the particular range of covid cases",style={'color':'#fff','text-align':'center'})
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-12')
    ],className='row'),
    html.Div([

         html.H1(style={'padding': '30'})
    ],className='row'),
    html.Div([

         html.H1(style={'padding': '30'})
    ],className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(id='picker1', options=options2, value='0-2000'),


            dcc.Graph(id='heatmap')
        ],className='col-md-12')
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='picker2', options=options2, value='0-2000'),


            dcc.Graph(id='box')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([

            dcc.Dropdown(id='picker3', options=options2, value='0-2000'),

            dcc.Graph(id='box1')
        ], className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([

            dcc.Dropdown(id='picker4', options=options2, value='0-2000'),

            dcc.Graph(id='box2')
        ], className='col-md-12')
    ],className='row'),
    html.Div([
         html.Div([

            dcc.Dropdown(id='picker5', options=options2, value='0-2000'),

            dcc.Graph(id='box3')
        ], className='col-md-12')
    ],className='row'), html.H4{[html.A("Back to home", href ="/")]}
],className='container')

@dhpp.callback(Output('heatmap','figure'),[Input('picker1','value')])
def update_graph(type1):
    bins = [0, 2000, 3000, 80000, 400000]
    data3 = data.copy()
    data3['confirmed'] = pd.cut(data3['confirmed'], bins, labels=['0-2000', '2001-3000', '3001-80000', '80000+'])
    new=data3[data3['confirmed']==type1]
    trace1=go.Box(x=new['HMT.current'],name='')
    return {'data':[trace1],'layout':go.Layout(title="Confirmed cases Vs Lead Exposure")}


@dhpp.callback(Output('box','figure'),[Input('picker2','value')])
def update_graph(type1):
    bins = [0, 2000, 3000, 80000, 400000]
    data3 = data.copy()
    data3['confirmed'] = pd.cut(data3['confirmed'], bins, labels=['0-2000', '2001-3000', '3001-80000', '80000+'])
    new = data3[data3['confirmed'] == type1]
    trace=go.Box(x=new['WRS.current'],name='',marker={'color':'#00a65a'})

    return {'data': [trace], 'layout': go.Layout(title="Confirmed cases Vs Wastewater Treament",xaxis={'title':'Water Percentage'},yaxis={'title':'Confirmed cases'})}


@dhpp.callback(Output('box1','figure'),[Input('picker3','value')])
def update_graph(type1):
    bins = [0, 2000, 3000, 80000, 400000]
    data3 = data.copy()
    data3['confirmed'] = pd.cut(data3['confirmed'], bins, labels=['0-2000', '2001-3000', '3001-80000', '80000+'])
    new = data3[data3['confirmed'] == type1]
    trace=go.Box(x=new['AGR.current'],name='',marker={'color':'#FF4136'})
    return {'data': [trace], 'layout': go.Layout(title="Confirmed cases Vs Sustainable Nitrogen",xaxis={'title':'Sustainable Nitrogen Percentage'},yaxis={'title':'Confirmed cases'})}


@dhpp.callback(Output('box2', 'figure'), [Input('picker4', 'value')])
def update_graph(type1):
    bins = [0, 2000, 3000, 80000, 400000]
    data3 = data.copy()
    data3['confirmed'] = pd.cut(data3['confirmed'], bins, labels=['0-2000', '2001-3000', '3001-80000', '80000+'])
    new = data3[data3['confirmed'] == type1]
    trace = go.Box(x=new['Wind Speed'], name='', marker={'color': '#FF851B'})

    return {'data': [trace],'layout': go.Layout(title="Confirmed cases Vs Wind Speed", xaxis={'title': 'Wind Speed'},yaxis={'title': 'Confirmed cases'})}

@dhpp.callback(Output('box3', 'figure'), [Input('picker5', 'value')])
def update_graph(type1):
    bins = [0, 2000, 3000, 80000, 400000]
    data3 = data.copy()
    data3['confirmed'] = pd.cut(data3['confirmed'], bins, labels=['0-2000', '2001-3000', '3001-80000', '80000+'])
    new = data3[data3['confirmed'] == type1]
    trace = go.Box(x=new['FRT.current'], name='', marker={'color': '#3D9970'})

    return {'data': [trace],'layout': go.Layout(title="Confirmed cases Vs Tree Cover", xaxis={'title': 'Tree Cover Percentage'},yaxis={'title': 'Confirmed cases'})}











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
    d = {'windspeed': 0, 'humidity': 0, 'temp':0, 'class': 0, 'prediction':0}
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
    return redirect('/pathname')


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
        prediction = model.predict(np.array([[humidity, temp, windspeed]]))
        output = round(prediction[0], 2)
        print(output)        

        d= {"windspeed": windspeed, "humidity": humidity, "temp":temp, "class": 1, 'prediction': int(output)}


        return d

api.add_resource(WeatherPred, "/api/<con>")