from flask import Flask, render_template, request
import json
import plotly.graph_objects as go
import sqlite3
from consultasMIS import *

app =  Flask(__name__)

@app.route("/")
def home():
    return '<p>Home Page</p>'

@app.route("/ips")
def ips():
    nips = request.args.get("ips",default=10,type=int)
    ips_sorted = getTopIps(nips)
    ip_alerts_plot = []
    ip_name = []
    for ip in ips_sorted:
        ip_alerts_plot.append(ip[1])
        ip_name.append(ip[0])
    fig = go.Figure(data=[go.Bar(y=ip_alerts_plot,x=ip_name)],
                    layout_title_text='TOP 10 IPS ALERTS',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)


@app.route("/vulnerables")
def dispositivos():
    ndispositivos = request.args.get("dispositivos",default=10,type=int)
    ids, values = getDispositivosVulnerables(ndispositivos)
    fig = go.Figure(data=[go.Table(header=dict(values=['ID',"TOTAL"]),cells= dict(values=[ids,values]))]
                    ,layout_title_text='ALERTS BY DEVICE',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)


@app.route("/peligrosos")
def peligrosos():
    peligrosos = request.args.get("peligrosos",default=False,type= lambda v:v.lower()=='true')
    top = request.args.get("top",default=5,type=int)
    ids, values = getDispositivosPeligrosos(peligrosos,top)
    fig = go.Figure(data=[go.Table(header=dict(values=['ID',"TOTAL"]),cells= dict(values=[ids,values]))]
                    ,layout_title_text='ALERTS BY DEVICE',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('peligrosos.html',graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug = True)

