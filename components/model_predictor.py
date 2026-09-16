import streamlit as st 
import pandas as pd 
import numpy as np 
import pickle
def predict(text):
    vectorizer=pickle.load(open("components/vectorizer.pkl","rb"))
    model=pickle.load(open("components/spam_model.pkl","rb"))
    vectorized_text=vectorizer.transform([text])
    result=model.predict(vectorized_text)
    probability=model.predict_proba(vectorized_text)
    return result[0],probability


