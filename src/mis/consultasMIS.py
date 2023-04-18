import pandas as pd
import sqlite3
import math
import requests
import json

def loadDataframe(query,conn):
    dataframe = pd.read_sql(query,conn)
    return dataframe

def getTopIps(nips):
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT origen FROM alertas where prioridad=1",conn)
    ips = dict()
    for i in range(0,len(dataframe)):
        if dataframe['origen'][i] in ips: ips[dataframe['origen'][i]] += 1
        else: ips[dataframe['origen'][i]] = 1
    maximo = 0
    for ip in ips:
        if ips[ip]>maximo: maximo=ips[ip]
    ips_sorted = sorted(ips.items(), key= lambda x:x[1], reverse=True)
    #CERRAR CONEXION
    conn.close()
    return ips_sorted[:nips]


def getDispositivosVulnerables(ndispositivos):
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT devices.id, analisis.servicios_inseguros, analisis.vulnerabilidades_detectadas FROM devices INNER JOIN analisis ON devices.id=analisis.id_device",conn)
    values = dict()
    for i in range(0,len(dataframe)):
        values[dataframe['id'][i]] = dataframe['servicios_inseguros'][i] + dataframe['vulnerabilidades_detectadas'][i]
    values_sorted = sorted(values.items(), key= lambda x:x[1], reverse=True)
    ids = []
    value_id = []
    if ndispositivos>len(values_sorted): ndispositivos = len(values_sorted) 
    for i in range(0,ndispositivos):
        ids.append(values_sorted[i][0])
        value_id.append(values_sorted[i][1])
    #CERRAR CONEXION
    conn.close()
    return ids, value_id

def getDispositivosPeligrosos(peligrosos,top):
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT devices.id, analisis.servicios_inseguros, analisis.servicios FROM devices INNER JOIN analisis ON devices.id=analisis.id_device",conn)
    values = dict()
    for i in range(0,len(dataframe)):
        values[dataframe['id'][i]] = dataframe['servicios_inseguros'][i]/dataframe['servicios'][i]
    values_sorted = sorted(values.items(), key= lambda x:x[1], reverse=True)
    ids = []
    value_id = []
    if top>len(values_sorted): top = len(values_sorted) 
    count = 0
    i=0
    if(peligrosos):
        while count<top and i<len(values_sorted):
            if values_sorted[i][1] >= 0.33:
                ids.append(values_sorted[i][0])
                value_id.append(values_sorted[i][1])
                count+=1
            i+=1
            
    else:
        while count<top and i<len(values_sorted):
            if values_sorted[i][1] < 0.33:
                ids.append(values_sorted[i][0])
                value_id.append(values_sorted[i][1])
                count+=1
            i+=1
    #CERRAR CONEXION
    conn.close()
    return ids, value_id


def getLastCVE(n=10):
    url = "https://cve.circl.lu/api/last"
    response = requests.get(url).json()
    ids = []
    modificiones = []
    resumenes = []
    for element in response:
        idCVE = element['id']
        ids.append(idCVE)
        modificada = element['last-modified']
        modificiones.append(modificada)
        sumary = element['summary']
        resumenes.append(sumary)
        references = element['references']
    return ids[:n], modificiones[:n], resumenes[:n]