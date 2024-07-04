import streamlit as st
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import SmartDataframe
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt




st.set_page_config(layout='wide')
st.title("Ask your CSV")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)

# Upload multiple CSV files
input_csv = st.sidebar.file_uploader(" ", type=['csv'], accept_multiple_files=False)

if input_csv:

    #load and display the selected csv file 
    st.success("CSV uploaded successfully")
    data = pd.read_csv(input_csv)
    st.dataframe(data, use_container_width=True)

    #Enter the query for analysis
    st.info("Chat Below")
    input_text = st.text_area("Enter the query")