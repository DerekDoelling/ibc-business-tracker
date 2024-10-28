import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# st.set_page_config(page_title='Traffic Dashboard', page_icon='📊')
st.title('Traffic Dashboard')

def app():

    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        
        st.write("This dashboard provides a comprehensive analysis of sales and traffic data over specified dates and hours. Each chart offers insights into different aspects of the data, helping you to understand the patterns and trends. The filter is on the far lefthand side of the screen.")
        st.write(f"Summary of the dashboard:  \n- First table is the raw data from the Daily Business Hour sheet   \n- The next table is a numerical summary showing the average, medium, and standard devation of traffic   \n- The following charts give insights into when customers are mostly likely to walk by. This can help workers to be prepared for the potential increase in demand.")
    
        # Load data
        dataframe = pd.read_excel(uploaded_file, sheet_name=['Daily Business Hours'])
        df = dataframe['Daily Business Hours']
        
        # Sidebar filters
        st.sidebar.header('Filters')
        date_range = st.sidebar.date_input('Date range', value=[df['Date'].min().date(), df['Date'].max().date()])
        
        # Display DataFrame
        st.subheader("Daily Business Hours")
        st.dataframe(df)
        
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create line graph for total sales throughout the dates
        st.title("Sales and Traffic Analysis")
        
        # Create bar chart for total sales for each hour of the day
        st.subheader("Total Sales for Each Hour of the Day")
        hourly_sales = df.groupby('Hour')['Sales per Hour'].sum().reset_index()
        # st.dataframe(hourly_sales)
        hourly_sales_graph = px.bar(hourly_sales, x=hourly_sales['Hour'], y=hourly_sales['Sales per Hour'], labels={'x': 'Hour', 'y': 'Total Sales'}, color_discrete_sequence=['#F63366'])
        hourly_sales_graph.update_traces(hovertemplate='Total Sales: $%{y:,.2f}<br>Hour: %{x}<extra></extra>')
        hourly_sales_graph.update_yaxes(tickformat="$,.0f")
        st.plotly_chart(hourly_sales_graph)

        # fig, ax = plt.subplots()
        # hourly_sales.plot(kind='bar', ax=ax)
        # ax.set_ylabel('Total Sales ($)')
        # # ax.set_title('Total Sales by Hour')
        # ax.tick_params(axis='x', rotation=0)  # Make x-axis reg
        # st.pyplot(fig)
        
        
        # Show traffic turnover from customer traffic to stop traffic
        st.subheader("Traffic Turnover Analysis")
        turnover_stats = df[['Customer Traffic', 'Stop Traffic']].describe().loc[['mean', '50%', 'std', 'min', 'max']]
        turnover_stats.index = ['Average', 'Median', 'Standard Deviation', 'Minimum', 'Maximum']
        st.table(turnover_stats)
        
        # Customer traffic over hours line chart
        st.subheader("Customer Traffic Over Hours")
        # fig, ax = plt.subplots()
        customer_traffic = df.groupby('Hour')['Customer Traffic'].mean() # .plot(ax=ax, marker='o')
        customer_traffic_graph = px.line(customer_traffic, x=customer_traffic.index, y=customer_traffic.values, markers=True, labels = {'x': 'Hour', 'y': 'Average Customer Traffic'}, color_discrete_sequence=['#F63366'])
        customer_traffic_graph.update_traces(hovertemplate='Average Customer Traffic: %{y:.2f}</b><br>Hour: %{x}<extra></extra>')
        customer_traffic_graph.update_yaxes(tickformat=",.0f")
        st.plotly_chart(customer_traffic_graph)
        # ax.set_ylabel('Average Customer Traffic')
        # ax.set_title('Customer Traffic by Hour')
        # st.pyplot(fig)
        
        # Additional charts if relevant
        # For example, let's create a line chart for Stop Traffic over Hours
        st.subheader("Stop Traffic Over Hours")
        # fig, ax = plt.subplots()
        stop_traffic = df.groupby('Hour')['Stop Traffic'].mean() #.plot(ax=ax, marker='o', color='red')
        stop_traffic_graph = px.line(stop_traffic, x=stop_traffic.index, y=stop_traffic.values, markers=True, labels = {'x': 'Hour', 'y': 'Average Stop Traffic'}, color_discrete_sequence=['#F63366'])
        stop_traffic_graph.update_traces(hovertemplate='Average Stop Traffic: %{y:.2f}</b><br>Hour: %{x}<extra></extra>')
        stop_traffic_graph.update_yaxes(tickformat=",.0f")
        st.plotly_chart(stop_traffic_graph)
        # ax.set_ylabel('Average Stop Traffic')
        # ax.set_title('Stop Traffic by Hour')
        # st.pyplot(fig)
        
        # Extract day of the week
        df['DayOfWeek'] = df['Date'].dt.day_name()
        
        # Filter for weekdays (Monday to Friday)
        weekday_data = df[df['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        
        # Customer and Stop Traffic over the days of the week
        st.subheader("Customer and Stop Traffic Over Days of the Week")
        
        # fig, ax = plt.subplots()
        cust_traff = weekday_data.groupby('DayOfWeek')['Customer Traffic'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) #.plot(ax=ax, marker='o', label='Customer Traffic')
        stop_traff = weekday_data.groupby('DayOfWeek')['Stop Traffic'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) #.plot(ax=ax, marker='o', color='red', label='Stop Traffic')
        cust_stop_traff = pd.merge(cust_traff, stop_traff, on = 'DayOfWeek')
        cust_stop_traff_graph = px.line(cust_stop_traff, x=cust_stop_traff.index, y=cust_stop_traff['Customer Traffic'], labels={'x': 'Day of the Week', 'y': 'Average Traffic'}, color = )
        cust_stop_traff_graph.update_traces(hovertemplate='Average Customer Traffic: %{y:.2f}</b><br>Day of the Week: %{x}<extra></extra>')
        cust_stop_traff_graph.update_yaxes(tickformat=",.0f")
        st.plotly_chart(cust_stop_traff_graph)
        # ax.set_ylabel('Average Traffic')
        # ax.set_title('Customer and Stop Traffic by Day of the Week')
        # ax.set_xlabel('Day of the Week')
        # ax.legend()
        # st.pyplot(fig)
        
    else:
        st.info("Please upload an Excel file on the Home page to get started")
