# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 20:08:41 2021

@author: Swapnanil Goswami
"""
from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)
pickle_in = open('regression_pred.pkl', 'rb')
detector1 = pickle.load(pickle_in)
pickle_in2 = open('classifier.pkl', 'rb')
detector2 = pickle.load(pickle_in2)

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict', methods = ["Get"])
def predict_rms_value():
    
    """ Let's claculate the RMS value of vibration and predict the state of working of the Smart Lathe Machine 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: cutting_speed
        in: query
        type: number
        required: true
      - name: feed
        in: query
        type: number
        required: true
      - name: depth_of_cut
        in: query
        type: number
        required: true
      - name: rpm
        in: query
        type: number
        required: true
      - name: diameter
        in: query
        type: number
        required: true
    responses:
        200:
            description: The prediction of the model is 
        
    """
    
    cutting_speed = request.args.get('cutting_speed')
    feed = request.args.get('feed')
    depth_of_cut = request.args.get('depth_of_cut')
    rpm = request.args.get('rpm')
    diameter = request.args.get('diameter')
    prediction1 = detector1.predict([[cutting_speed, feed, depth_of_cut, rpm, diameter]])
    prediction2 = detector2.predict(abs(prediction1))
    print(prediction2)
    if prediction2[0] == 1 and (abs(prediction1[0]) <= 373.0):
        return "Machine will work fine with the given parameters"
    
    if prediction2[0] == 1 and (abs(prediction1[0]) > 373.0):
        return "Machine might or might not produce faults"

    if prediction2[0] == 0 or (abs(prediction2[0]) > 390.0):
        return "The given set of parameters will definitely produce faults"



if __name__ == '__main__':
    app.run()
