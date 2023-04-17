import streamlit as st 
import pandas as pd 


@st.cache_resource
def get_data ():
    path = "Emissions.xlsx"
    return pd.read_excel(path,sheet_name="Sheet1",usecols="A:F")

data = get_data()


#select dropdown 
scope = data.columns.tolist()
select_scope = st.selectbox('select scope:',scope)
column_values = data[select_scope].unique()
selected_column = st.selectbox("Select Scope:",column_values)
fuel = data[selected_column].tolist()

