import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
from pandasai import SmartDataframe
import seaborn as sns


openai_api_key = ''


# Function to handle user queries
def chat_with_csv(df, prompt):
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    result = pandas_ai.chat(prompt)
    return result

def generate_statistics(data):
    stats = {}
    
    # Basic Statistics
    stats['Basic Statistics'] = data.describe().T
    
    # Null Values
    null_values = data.isnull().sum()
    null_percentage = (null_values / len(data)) * 100
    stats['Null Values'] = pd.DataFrame({'Null Values': null_values, 'Percentage': null_percentage})
    
    # Data Types
    stats['Data Types'] = pd.DataFrame(data.dtypes, columns=['Data Type'])
    
    # Unique Values
    unique_values = data.nunique()
    stats['Unique Values'] = pd.DataFrame({'Unique Values': unique_values})
    
    return stats

# Streamlit app layout and settings
st.set_page_config(layout='wide')
st.title("Ask your CSV")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)

# Upload CSV file
input_csv = st.sidebar.file_uploader(" ", type=['csv'], accept_multiple_files=False)

if input_csv:
    data = pd.read_csv(input_csv)
    st.success("CSV uploaded successfully")
    
    # Sidebar options
    view_option = st.sidebar.radio(
        "View Options",
        ('Data Preview', 'Chat With CSV')
    )
    
    if view_option == 'Data Preview':
        st.subheader("Data Preview")
        st.dataframe(data, use_container_width=True)
    

        st.subheader("Basic statistical metrics about your uploaded csv")
        stats = generate_statistics(data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Statistics")
            st.dataframe(stats['Basic Statistics'])
        
        with col2:
            st.subheader("Null Values")
            st.dataframe(stats['Null Values'])
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Data Types")
            st.dataframe(stats['Data Types'])
        
        with col4:
            st.subheader("Unique Values")
            st.dataframe(stats['Unique Values'])
        
        st.subheader("Correlation Matrix")
        corr_matrix = data.corr()
        fig, ax = plt.subplots(figsize=(4, 2))
        heatmap = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax, annot_kws={"size": 4}, cbar_kws={"shrink": 1})
        cbar = heatmap.collections[0].colorbar
        cbar.ax.tick_params(labelsize=4)
        plt.xticks(fontsize=4)
        plt.yticks(fontsize=4)
        st.pyplot(fig)

    
    elif view_option == 'Chat With CSV':
        st.subheader("Data Preview")
        st.dataframe(data, use_container_width=True)
    
        # User query input
        st.info("Chat Below")
        input_text = st.text_area("Enter the query")

        if input_text:
            result = chat_with_csv(data, input_text)
            fig_number = plt.get_fignums()
            if fig_number:
                st.pyplot(plt.gcf())
            else:
                st.success(result)