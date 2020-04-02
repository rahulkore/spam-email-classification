from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker

import csv
from urllib.request import urlopen
from json import load
import gmplot
from collections import defaultdict



import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

#engine = create_engine('sqlite:///tutorial.db', echo=True)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/after_mail_entry",methods=["POST"])
def after_mail_entry():
    email = request.form["email"]
    addr = request.form["ip"]
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    #will load the json response into data
    latlong=data['loc'].split(',')
    lat=latlong[0]
    long=latlong[1]

    location=str(data['city'])+','+str(data['region'])+','+str(data['country'])
    #print(location)
    #print(lat)
    #print(long)

    for attr in data.keys():
        #will print the data line by line
        print(attr,' '*13+'\t->\t',data[attr])



    output_field_names=['latitude','longitude','location']
    output_filename="data_op.csv"

    with open(output_filename,'a',newline="\n") as csvoutput:
        writer=csv.DictWriter(csvoutput,fieldnames=output_field_names)

        # if it's an empty file, write the header
        if os.stat(output_filename).st_size == 0:
            writer.writeheader()

        op={'latitude':lat,'longitude':long,'location':location}

        writer.writerow(op)

        csvoutput.close()


    #url = "https://steel-earth-269715.appspot.com/register/"+email
    url = "http://127.0.0.1:4000/register/"+email
    import requests
    request_url = requests.get(url)
    #result = request_url.read()
    print(request_url.text)

    return render_template("after_home.html",email=email,result = request_url.text,addr=addr)
    #return email

@app.route("/heatmaps")
def heatmaps():
    #return "rahul"
    raw_data = pd.read_csv("data_op.csv")

    latitudes=raw_data['latitude']

    longitudes=raw_data['longitude']
    #return str(latitudes)+str(longitudes)
    gmap = gmplot.GoogleMapPlotter(19.0728, 72.8826, 10)

    gmap.heatmap(latitudes, longitudes)

    gmap.draw("my_heatmap.html")
    #return "ok"
    return render_template("my_heatmap.html")

@app.route("/bargraph")
def bargraph():

    raw_data=pd.read_csv("data_op.csv")
    locations=raw_data['location']
    city_dict=defaultdict(int)
    state_dict=defaultdict(int)
    country_dict=defaultdict(int)
    #print(locations)
    for i in raw_data.index:
        #print(raw_data['location'][i])
        csc=raw_data['location'][i].split(',')
        city=csc[0]
        state=csc[1]
        country=csc[2]

        city_dict[city]+=1
        state_dict[state]+=1
        country_dict[country]+=1
    #print(city_dict,state_dict,country_dict)
    print(city_dict,state_dict,country_dict)
    return render_template("bargraph.html",city_dict=city_dict,state_dict=state_dict,country_dict=country_dict)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4555)
