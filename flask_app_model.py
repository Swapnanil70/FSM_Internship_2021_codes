# -*- coding: utf-8 -*-
"""
Created on July 25th 
@author: Swapnanil Goswami
"""
from flask import Flask, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
pickle_in = open('regression_pred.pkl', 'rb')
detector = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"
@app.route('/predict')
def predict_rms_value():
    cutting_speed = request.args.get('cutting_speed')
    feed = request.args.get('feed')
    depth_of_cut = request.args.get('depth_of_cut')
    rpm = request.args.get('rpm')
    diameter = request.args.get('diameter')
    prediction = detector.predict([[cutting_speed, feed, depth_of_cut, rpm, diameter]])
    return "The prediction " + str(prediction)









if __name__ == '__main__':
    app.run()
