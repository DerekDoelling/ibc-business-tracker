import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

def app():
    st.title('IBC Dashy 📊')
# Data Explorer Dashboard
    with st.expander('About this app'):
        st.markdown('**What can this app do?**')
        st.markdown('This app allows you to explore and analyze business data from Excel files.')
        st.markdown('**How to use the app?**')
        st.warning('To engage with the app:\n'
                   '1. Upload your Excel sheet\n'
                   '2. Navigate through different sections using the sidebar.\n'
                   '2. Explore the dashboard')

    st.header("Introduction")
    st.write("Welcome to the IBC Dashy web app. This tool allows you to upload and analyze business data from Excel files. The app supports various data visualizations and summaries to help you understand your business metrics better.")

    st.header("Upload Excel File")
    uploaded_file = st.file_uploader("", type=["xlsx"])

    # def plot_line_chart(df, title):
    #     plt.figure(figsize=(10, 6))
    #     sns.lineplot(data=df, x=df["Date"], y=df["Stop Traffic"])
    #     plt.title(title)
    #     plt.xlabel('Date')
    #     plt.ylabel('Stop Traffic')
    #     plt.xticks(rotation=45)
    #     st.pyplot(plt)

    if uploaded_file is not None:
        # Store the file in session state
        st.session_state.uploaded_file = uploaded_file
        df = pd.read_excel(uploaded_file)
        
        progress_bar = st.progress(0)

        for per_completed in range(100):
            time.sleep(0.0005)
            progress_bar.progress(per_completed + 1)

            if per_completed == 99:
                st.markdown("""
                <style>
                .stProgress > div > div > div > div {
                    background-color: green;
                }
                </style>
                """, unsafe_allow_html=True)

        st.success("File Uploaded Successfully!")
        st.write("You can click on the different dashboards on the left under ***Navigation*** to see the different dashboards.")
        
        # df = pd.read_excel(uploaded_file, skiprows=1, usecols=list(range(1, 17))) #"Year", "Smstr", "#", "Company Name", "Primary Location", "Rent/Domain Amount  for Primary Location", "Description", "Revenue", "COGS", "Gross Profit", "Gross Margin", "Operating Expenses", "Operating Income", "Net Income", "Ending Cash Balance", "Net Income Margin"])

        # st.subheader("Data Preview")
        # st.write(df.tail())

        # st.subheader("Data Summary")
        # st.write(df.describe())

    #     # Read the uploaded file
    #     df = pd.read_excel(uploaded_file, sheet_name=["Daily Business Hours", "Inventory", "Sales", "Member Actions"])
    #     dbh_df = df['Daily Business Hours']
    #     inv_df = df["Inventory"]
    #     sale_df = df["Sales"]
    #     member_df = df["Member Actions"]

    #     st.write("Data from the uploaded file:")
    #     st.dataframe(dbh_df)

    #     st.header("Line Chart")
    #     plot_line_chart(dbh_df, "Daily Business Hours Line Chart")
    # else:
    #     st.header("Demo")
    #     st.write("Example on Dummy Data")

    #     # Example with dummy data if no file is uploaded
    #     df = pd.read_excel('data/IBC_Static_Data.xlsx', sheet_name=["Daily Business Hours", "Inventory", "Sales", "Member Actions"])
    #     dbh_df = df['Daily Business Hours']
    #     inv_df = df["Inventory"]
    #     sale_df = df["Sales"]
    #     member_df = df["Member Actions"]

    #     st.write("How a Data Frame Looks")
    #     st.dataframe(dbh_df)

    #     st.write("Line Chart")
    #     plot_line_chart(dbh_df, "Dummy Data Line Chart")

    st.markdown("[GitHub Repository](https://github.com/TylerEnglish/ibc-business-tracker)")



def main():

    print("gu")



if __name__ == "__main__":
    app()