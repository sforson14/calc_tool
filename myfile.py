import sys
sys.path.insert(1, "/Users/stephenforson/.local/share/virtualenvs/Calc_tool-n54-u4Hm/lib/python3.9/site-packages")
from streamlit_option_menu import option_menu

import streamlit as st 
import pandas as pd 
from streamlit_option_menu import option_menu


#------- PAGE SETTINGS------------
page_title = "GHG Emission Calculator"
Page_icon = "🌳"
layout = "centered"

#-----------------------------------
st.set_page_config(page_title=page_title,page_icon=Page_icon,layout=layout)
st.title(page_title + " " + Page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)


@st.cache_resource
def get_data ():
    path = "Emissions.xlsx"
    return pd.read_excel(path,sheet_name="Sheet2",usecols="A:I")

#----remember to remove duplicates
data = get_data()
data_na = data.dropna()


options1 = data_na.iloc[:,0].unique()
selected_option1 = st.selectbox("Select Scope:",options1)

#----filtering scope-------
filtered_data = data_na[data_na.iloc[:,0]==selected_option1]

#----get unique values for option 2-----
option2 = filtered_data.iloc[:,1].unique()
selected_option2 = st.selectbox("Select Category:",option2)

#-----filter based on option 2-----
filter_2 = filtered_data[filtered_data.iloc[:,1]==selected_option2]
option3 = filter_2.iloc[:,2].unique()
selected_option3 = st.selectbox("Select Sub Category:",option3)

#----filter based on option 3----
filter_3 = filter_2[filter_2.iloc[:,2]== selected_option3]
option4 = filter_3.iloc[:,3].unique()
selected_option4 = st.selectbox("Select Material:",option4)

#-----filter based on option 4----
filter_4 = filter_3[filter_3.iloc[:,3]==selected_option4]
option5 = filter_4["UOM"].unique()
selected_option5 = st.selectbox("Select Unit of Measure:",option5)

#----filter based on option 5-------
filter_5 = filter_4[filter_4["UOM"]== selected_option5]
option6 = filter_5["GHG/Unit"].unique()
selected_option6 = st.selectbox("Select Unit:",option6)

#-----filter based on last option-----
filter_6 = filter_5[filter_5["GHG/Unit"]== selected_option6]
option_7 = filter_6["GHG Conversion Factor 2022"].unique()
selected_option7 = st.selectbox("Emission Factor:",option_7)
#option7_int = int(selected_option7)

#----create an input field-------
with st.form("my_form", clear_on_submit=True):
    values = st.number_input("Enter Amount",format="%i",min_value=0)
    values_int = int(values)

#----multiplying the two columns together to find total emission----

    emission = int(selected_option7 * values_int)

    total = st.number_input("Total Emissions:",emission)

    #---Creating the submit button------------- 
    submitted = st.form_submit_button("Save Data")
    if submitted:
        st.write("scope:",selected_option1)


