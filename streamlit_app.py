import streamlit as st
import numpy as np
import pandas as pd
import openpyxl

# Page title
st.set_page_config(page_title='IBC Data Explorer Dashboard', page_icon='📊')
st.title('📊 IBC Data Explorer Dashboard')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Matplotlib for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Upload your excel sheet and then 2. Select the date duration from the slider widget. 3. Explore the dashboard to find insights!')
  
st.subheader('Data Dashboard')

# Load data
df = pd.read_excel('data\Student_Business_Test2.xlsx', sheet_name=["Daily Business Hours", "Inventory", "Sales", "Member Actions"])
dbh_df = df['Daily Business Hours']
inv_df = df["Inventory"]
sale_df = df["Sales"]
member_df = df["Member Actions"]

st.write(dbh_df)

