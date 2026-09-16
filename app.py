import streamlit as st 
from components.model_predictor import predict


st.title("SMS spam detection")


text=st.text_input("Enter your message : ")
if st.button("Predict"):
    st.spinner("predicting....")
    predic,prob=predict(text=text)
    if(predic==0):
        st.success("Ham message")
    else:
        st.error("SPAM message")
    st.write(f"the Prediction the Model for HAM : {prob[0][0]*100}.2f %")
    st.write(f"the Prediction the Model for SPAM : {prob[0][1]*100}2f %")