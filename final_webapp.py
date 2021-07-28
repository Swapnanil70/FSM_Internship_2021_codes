# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 20:26:08 2021

@author: Swapnanil
"""
from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
import streamlit as st

from PIL import Image 

#app = Flask(__name__)
pickle_in = open('regression_pred.pkl', 'rb')
detector1 = pickle.load(pickle_in)
pickle_in2 = open('classifier.pkl', 'rb')
detector2 = pickle.load(pickle_in2)

#@app.route('/')
def welcome():
    return "Welcome All"
#@app.route('/predict')
def predict_fault(cutting_speed, feed, depth_of_cut, rpm, diameter):
    
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
    
    
    prediction1 = detector1.predict([[cutting_speed, feed, depth_of_cut, rpm, diameter]])
    prediction2 = detector2.predict(abs(prediction1))
    if prediction2[0] == 1 and (abs(prediction1[0]) <= 373.0):
        return "Machine will work fine with the given parameters, which produces RMS value of " + str(prediction1[0])
    
    if prediction2[0] == 1 and ((abs(prediction1[0]) > 373.0 and (abs(prediction1[0]) < 390.0))):
        return "Machine might or might not produce faults, because the RMS value of " + str(prediction1[0]) + " has exceded the Threshold value by some margin "

    if prediction2[0] == 0 or (abs(prediction1[0]) > 390.0):
        return "The given set of parameters will definitely produce faults, because the RMS value of " + str(prediction1[0]) + " has exceded the Threshold value by a large margin "

def main():
    st.title("Fault Detection of Smart Lathe Machine")
    st.title("Vibration RMS Authenticator")
    html_temp = """
    <div style="background-color:purple;padding:10px">
    <h2 style="color:white;text-align:center;">Fault Detection of Smart Lathe Machine </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    cutting_speed = st.text_input("cutting_speed", "Type_Here")
    feed = st.text_input("feed", "Type_Here")
    depth_of_cut = st.text_input("depth_of_cut", "Type_Here")
    rpm = st.text_input("rpm", "Type_Here")
    diameter = st.text_input("diameter", "Type_Here")
    result=""
    if st.button("Predict"):
        result = predict_fault(cutting_speed, feed, depth_of_cut, rpm, diameter)
    st.success('The prediction of the model is :- {}'.format(result))
    if st.button("About"):
        st.text("Model built using sklearn")
        st.text("Built UI with Streamlit")

if __name__ == '__main__':
    main()

