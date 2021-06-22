from io import BytesIO
from flask import Flask, request, render_template
from flask.globals import request
from flask.templating import render_template
## For analzye
import base64
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import date
import datetime as dt

df = pd.read_csv('buy_vip.csv')


app = Flask(__name__)

@app.route("/")
def index():
    today = date.today()
    last_day= (today - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    d1 = today.strftime("%Y-%m-%d")
    week_Ago = today - dt.timedelta(days=8)
    week_ago = week_Ago.strftime("%Y-%m-%d")
    mask = (df['Date'] > week_ago) & (df['Date'] <= last_day)
    selected_df = df.loc[mask]
    date_line = selected_df['Date']
    count_buy = selected_df['Buy']
    date_label = [label[5:] for label in date_line ]
    fig = Figure()
    ax = fig.subplots()
    ax.title.set_text('Günlere Göre VIP Üyelik Satın Alma')
    #plt.rcParams.update({'font.size': 13})
    ax.plot(date_label, count_buy, marker = 'o')
    ax.set_xticklabels(date_label, rotation = 60)
    ax.set_yticks(range(count_buy.max()+1))
    ax.set_xlabel('Tarih')
    ax.set_ylabel('VIP Üyelik Satın Alma')
    ax.yaxis.grid()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    current_data = base64.b64encode(buf.getbuffer()).decode("ascii") 

    calender = {
        "date" : d1,
        "data": current_data
    }
    return render_template("index.html", calender=calender)

@app.route("/show", methods = ['POST'])
def show():
    today = date.today()
    d2 = today.strftime("%Y-%m-%d")

    start_d = str(request.form.get("start_date"))
    end_d = str(request.form.get("end_date"))
    mask = (df['Date'] > start_d) & (df['Date'] <= end_d)
    selected_df = df.loc[mask]
    date_line = selected_df['Date']
    count_buy = selected_df['Buy']
    date_label = [label[5:] for label in date_line ]
    fig = Figure()
    ax = fig.subplots()
    ax.title.set_text('Günlere Göre VIP Üyelik Satın Alma')
    #plt.rcParams.update({'font.size': 13})
    ax.plot(date_label, count_buy, marker = 'o')
    ax.set_xticklabels(date_label, rotation = 60)
    ax.set_yticks(range(count_buy.max()+1))
    ax.set_xlabel('Tarih')
    ax.set_ylabel('VIP Üyelik Satın Alma')
    ax.yaxis.grid()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii") 
    
    
    result = {
        "data" : data,
        "date" : d2
    }
    return render_template("index.html", result = result)

if __name__ == "__main__":
    app.run(debug=True)

