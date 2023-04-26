from flask import Flask, render_template, request
import json
import plotly.graph_objects as go
import sqlite3
from consultasMIS import *

app =  Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/ips", methods=["GET", "POST"])
def ips():
    nips = request.args.get("ips",default=10,type=int)
    ips_sorted = getTopIps(nips)
    ip_alerts_plot = []
    ip_name = []
    for ip in ips_sorted:
        ip_alerts_plot.append(ip[1])
        ip_name.append(ip[0])
    fig = go.Figure(data=[go.Bar(y=ip_alerts_plot,x=ip_name)],
                    layout_title_text=f'TOP {nips} IPS ALERTS',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)


@app.route("/vulnerables", methods=["GET", "POST"])
def dispositivos():
    ndispositivos = request.args.get("dispositivos",default=10,type=int)
    ids, values = getDispositivosVulnerables(ndispositivos)
    fig = go.Figure(data=[go.Table(header=dict(values=['ID',"TOTAL"]),cells= dict(values=[ids,values]))]
                    ,layout_title_text='DEVICES',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)


@app.route("/peligrosos", methods=["GET", "POST"])
def peligrosos():
    peligrosos = request.args.get("peligrosos", default=False, type=lambda v: v.lower() == 'true')
    if request.method == "POST":
        top = request.form.get("top", default=7, type=int)
        peligrosos = request.form.get("peligrosos", default=False, type=lambda v: v.lower() == 'true')
    else:
        top = 7
    ids, values = getDispositivosPeligrosos(peligrosos, top)
    fig = go.Figure(data=[go.Table(header=dict(values=['ID', "TOTAL"]), cells=dict(values=[ids, values]))],
                    layout_title_text='ALERTS BY DEVICE', layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('peligrosos.html', graphJSON=graphJSON, peligrosos=peligrosos)


@app.route("/cve")
def cve():
    ids, modificada, resumen = getLastCVE()
    fig = go.Figure(data=[go.Table(header=dict(values=['ID',"MODIFICACION","RESUMEN"]),cells= dict(values=[ids,modificada, resumen]))]
                    ,layout_title_text='LAST 10 CVEs DETECTED',layout=go.Layout(height=1500))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)

@app.route("/check", methods=["POST"])
def checkUrl():

    url = request.form['url']
    apikey = request.form['apiKey']
    print (url, apikey)

    jsonObject = getURLScanned(url=url, apiKey=apikey)

    urlplot = jsonObject['data']['attributes']['url']
    lastUrlPlot = jsonObject['data']['attributes']['last_final_url']
    statsUrlPlot = jsonObject['data']['attributes']['last_analysis_stats']
    resultsUrlPlot = jsonObject['data']['attributes']['last_analysis_results']

    
    statsUrlPlot =  json.dumps(statsUrlPlot, indent=4)
    resultsUrlPlot = json.dumps(resultsUrlPlot, indent=1)

    fig = go.Figure(data=[go.Table(header=dict(values=["URL", "REDIRECCIÓN FINAL", "ÚLTIMOS STATS", "RESULTADOS"]),cells= dict(values=[urlplot, lastUrlPlot, statsUrlPlot, resultsUrlPlot]))]
                    ,layout_title_text='Pequeño análisis de la url.',layout=go.Layout(height=1500))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)

    return render_template('home.html',graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug = True)

