# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:27:14 2020

@author: Anish Parulekar
Template inspiration: @krishnaik - github
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rmdscmodel.pkl', 'rb'))
SC = pickle.load(open('scalarobject.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


sc = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Miles_Driven=int(request.form['Miles_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol =  0
        Age=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=model.predict(SC.transform([[Present_Price,Miles_Driven,Owner,Age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]]))
        output=round(prediction[0],0)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry, your car does not have a reasonable resell value")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at ${}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)