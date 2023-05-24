import streamlit as st 
import pandas as pd 
import plotly.express as px
from deta import Deta
import sys
from streamlit_option_menu import option_menu

#----connect database-----

deta = Deta(st.secrets["DETA_KEY"])

#-----name of database from deta-----

db = deta.Base("emissions")

#-----return all items in database-------
db_content = db.fetch().items

#----fetching scope category-----
def get_scope():
    items = db.fetch()
    scope = [item["Scope"]for item in items]


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

if selected == "Data Entry":
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
            selected_option1 = selected_option1
            selected_option2 = selected_option2
            selected_option3 = selected_option3
            selected_option4 = selected_option4
            values = values
            total = total
            st.success("Data Saved Successfully!")
            db.put({"Scope":selected_option1,"Category":selected_option2,"subCategory":selected_option3,"Material":selected_option4,"Quantity":values,"Total Emission":total})

#-------Get the data and plotting the graph---------------
if selected == "Data Visualization":
    #st.header("Emission Dashboard")
    #with st.form("Saved_scope"):
        #scope = st.selectbox("Select Scope:",get_scope())
        #submitted = st.form_submit_button("Plot Scope")

#-----Convert database into dictionary----------       
    df = pd.DataFrame.from_dict(db_content)
    category_name = "Scope"
    unique_cat = df[category_name].unique()
    #table = st.dataframe(df)


#--------side bar filter 

    st.sidebar.header("GHG Emissions Dashboard")
    st.sidebar.header("Please Filter Scope:")
    scope_cat = st.sidebar.selectbox(
        "Select Scope:",
        options=df[category_name].unique()
    )

    df_selection = df.query(
        "Scope == @scope_cat"
    )

    #------MAINPAGE-------
    st.title(":bar_chart: Emissions Dashboard")
    st.markdown("##")


    #--Emission KPI---

    tot_emission = int(df_selection["Total Emission"].sum())
    total_quantity = int(df_selection["Quantity"].sum())
    tot_emis = int(df["Total Emission"].sum())

    left_column,middle_column,right_column = st.columns(3)
    with left_column:
        st.subheader("Total Emissions Per Category:")
        st.subheader(f"{tot_emission:,} kgCO2e")
    with middle_column:
        st.subheader("Total Material Quantity")
        st.subheader(total_quantity)
    with right_column:
        st.subheader("Total Project Emissions")
        st.subheader(f"{tot_emis:,} kgCO2e")

    st.markdown("---")

    #-----Dashboard visual-------
    emission_by_material = (
        df_selection.groupby(by=["Material"]).sum()[["Total Emission"]].sort_values(by="Total Emission")
    )
    fig_emission_tot = px.bar(
     emission_by_material ,
     x= "Total Emission",
     y= emission_by_material.index,
     orientation="h",
     title="<b>Emissions by Material </b>",
     color_discrete_sequence=["#0083B8"]*len(emission_by_material),
     template="plotly_white",
    )

    st.plotly_chart(fig_emission_tot)






























    #st.dataframe(df_selection)



















    











