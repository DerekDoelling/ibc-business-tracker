import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# st.set_page_config(page_title='Traffic Dashboard', page_icon='📊')

def app():

    st.title('Traffic Dashboard 🚗')

    traffic_example = "data\\traffic_example.png"

    with st.expander('Help ✋'):
            st.markdown('***How does this work?***')
            st.markdown('This dashboard will automatically load all the data from the "Daily Business Hours" sheet in the Excel file you upload. It will then provide a summary table and insightful visualizations of the data.')
            st.markdown('***Why am I getting an error?***')
            st.markdown('If you are getting an error, please make sure that you are uploading the correct file. The file should be an excel file with a sheet named "Daily Business Hours".')
            st.markdown('Within the "Daily Business Hours" sheet, there should be these eight columns: Date, Hour, Staff on Duty, Traffic, Customer Traffic, Stop Traffic, Sales per Hour, and Event/Notes. You can add columns to the sheet, but you must have at least the specified columns.')
            st.image(traffic_example, caption = 'Example')

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
        # st.header("Sales and Traffic Analysis")
        
        # Create bar chart for total sales for each hour of the day
        st.header("Sales for Each Hour of the Day")
        hourly_sales = df.groupby('Hour')['Sales per Hour'].sum().reset_index()
        # st.dataframe(hourly_sales)
        hourly_sales_graph = px.bar(hourly_sales, x=hourly_sales['Hour'], y=hourly_sales['Sales per Hour'], labels={'x': 'Hour', 'y': 'Total Sales'}, color_discrete_sequence=['#F63366'])
        hourly_sales_graph.update_traces(hovertemplate='Hour: %{x}<br>Total Sales: <b>$%{y:,.2f}</b><extra></extra>')
        hourly_sales_graph.update_layout(xaxis_title='Hour', yaxis_title='Total Sales')
        hourly_sales_graph.update_yaxes(tickformat="$,.0f")
        hourly_sales_graph.update_xaxes(showgrid=False)
        hourly_sales_graph.update_yaxes(showgrid=False)
        hourly_sales_graph.update_yaxes(zeroline=False)
        st.plotly_chart(hourly_sales_graph)

        # fig, ax = plt.subplots()
        # hourly_sales.plot(kind='bar', ax=ax)
        # ax.set_ylabel('Total Sales ($)')
        # # ax.set_title('Total Sales by Hour')
        # ax.tick_params(axis='x', rotation=0)  # Make x-axis reg
        # st.pyplot(fig)

        st.header("Sales by Hour")
        hourly_sales_avg = df.groupby('Hour')['Sales per Hour'].mean().reset_index()
        # st.dataframe(hourly_sales_avg)
        hourly_sales_avg_graph = px.line(hourly_sales_avg, x=hourly_sales_avg['Hour'], y=hourly_sales_avg['Sales per Hour'], labels={'x': 'Hour', 'y': 'Average Sales'}, color_discrete_sequence=['#F63366'], markers = True)
        hourly_sales_avg_graph.update_traces(hovertemplate='Hour: %{x}<br>Average Sales: <b>$%{y:,.2f}</b><extra></extra>')
        hourly_sales_avg_graph.update_layout(xaxis_title='Hour', yaxis_title='Average Sales')
        hourly_sales_avg_graph.update_yaxes(tickformat="$,.0f")
        hourly_sales_avg_graph.update_xaxes(showgrid=False)
        hourly_sales_avg_graph.update_yaxes(showgrid=False)
        hourly_sales_avg_graph.update_yaxes(zeroline=False)

        st.plotly_chart(hourly_sales_avg_graph)        
        
        # Show traffic turnover from customer traffic to stop traffic
        st.header("Traffic Turnover Overview")
        turnover_stats = df[['Customer Traffic', 'Stop Traffic']].describe().loc[['mean', '50%', 'std', 'min', 'max']]
        turnover_stats.index = ['Average', 'Median', 'Standard Deviation', 'Minimum', 'Maximum']
        traffic_ratio = df.copy()
        traffic_ratio['ratio'] = traffic_ratio['Customer Traffic'] / traffic_ratio['Stop Traffic']
        traffic_ratio_number =  traffic_ratio['ratio'].mean()
        
        st.table(turnover_stats)
        st.write(f"The average ratio of customer traffic to stop traffic is ***{traffic_ratio_number:.1f}***.")

        st.header("Total Customer and Stop Traffic")
        customer_traffic = df['Customer Traffic'].sum()
        stop_traffic = df['Stop Traffic'].sum()
        traffic = pd.DataFrame({'Traffic Type': ['Customer Traffic', 'Stop Traffic'], 'Total Traffic': [customer_traffic, stop_traffic]})
        traffic = traffic.sort_values(by='Total Traffic', ascending=False)
        # st.dataframe(traffic)
        total_traffic_graph = px.bar(traffic, x='Traffic Type', y='Total Traffic', color='Traffic Type')
        total_traffic_graph.update_traces(hovertemplate='Traffic Type: %{x}<br>Total Traffic: <b>%{y:,.0f}</b><extra></extra>')
        total_traffic_graph.update_layout(xaxis_title='', yaxis_title='Total Traffic')
        total_traffic_graph.update_yaxes(tickformat=",.0f")
        total_traffic_graph.update_layout(showlegend=False)
        total_traffic_graph.update_xaxes(showgrid=False)
        total_traffic_graph.update_yaxes(showgrid=False)
        total_traffic_graph.update_yaxes(zeroline=False)

        st.plotly_chart(total_traffic_graph)

        # Customer traffic over hours line chart
        st.header("Customer Traffic by Hour")
        # fig, ax = plt.subplots()
        customer_traffic = df.groupby('Hour')['Customer Traffic'].mean() # .plot(ax=ax, marker='o')
        customer_traffic_graph = px.line(customer_traffic, x=customer_traffic.index, y=customer_traffic.values, markers=True, labels = {'x': 'Hour', 'y': 'Average Customer Traffic'}, color_discrete_sequence=['#F63366'])
        customer_traffic_graph.update_traces(hovertemplate='Hour: %{x}<br>Average Customer Traffic: <b>%{y:.2f}</b><extra></extra>')
        customer_traffic_graph.update_yaxes(tickformat=",.0f")
        customer_traffic_graph.update_xaxes(showgrid=False)
        customer_traffic_graph.update_yaxes(showgrid=False)
        customer_traffic_graph.update_yaxes(zeroline=False)
        st.plotly_chart(customer_traffic_graph)
        # ax.set_ylabel('Average Customer Traffic')
        # ax.set_title('Customer Traffic by Hour')
        # st.pyplot(fig)
        
        # Additional charts if relevant
        # For example, let's create a line chart for Stop Traffic over Hours
        st.header("Stop Traffic by Hour")
        # fig, ax = plt.subplots()
        stop_traffic = df.groupby('Hour')['Stop Traffic'].mean() #.plot(ax=ax, marker='o', color='red')
        stop_traffic_graph = px.line(stop_traffic, x=stop_traffic.index, y=stop_traffic.values, markers=True, labels = {'x': 'Hour', 'y': 'Average Stop Traffic'}, color_discrete_sequence=['#F63366'])
        stop_traffic_graph.update_traces(hovertemplate='Hour: %{x}<br>Average Stop Traffic: <b>%{y:.2f}</b><extra></extra>')
        stop_traffic_graph.update_yaxes(tickformat=",.0f")
        stop_traffic_graph.update_xaxes(showgrid=False)
        stop_traffic_graph.update_yaxes(showgrid=False)
        stop_traffic_graph.update_yaxes(zeroline=False)
        st.plotly_chart(stop_traffic_graph)
        # ax.set_ylabel('Average Stop Traffic')
        # ax.set_title('Stop Traffic by Hour')
        # st.pyplot(fig)
        
        # Extract day of the week
        df['DayOfWeek'] = df['Date'].dt.day_name()
        
        # Filter for weekdays (Monday to Friday)
        weekday_data = df[df['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        
        # Customer and Stop Traffic over the days of the week
        st.header("Customer and Stop Traffic by Day of the Week")
        
        # fig, ax = plt.subplots()
        cust_traff = weekday_data.groupby('DayOfWeek')['Customer Traffic'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) #.plot(ax=ax, marker='o', label='Customer Traffic')
        stop_traff = weekday_data.groupby('DayOfWeek')['Stop Traffic'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) #.plot(ax=ax, marker='o', color='red', label='Stop Traffic')
        cust_stop_traff = pd.merge(cust_traff, stop_traff, on = 'DayOfWeek')
        cust_stop_traff_df = cust_stop_traff.reset_index().melt(id_vars=['DayOfWeek'], var_name='Traffic Type', value_name='Average Traffic')        
        # st.dataframe(cust_stop_traff_df)

        cust_stop_traff_graph = px.line(cust_stop_traff_df, x='DayOfWeek', y='Average Traffic', color = 'Traffic Type', markers=True)
        cust_stop_traff_graph.update_traces(hovertemplate='Day of the Week: %{x}<br>Average Customer Traffic: <b>%{y:.2f}</b><extra></extra>')
        cust_stop_traff_graph.update_layout(xaxis_title='', yaxis_title='Average Traffic')
        cust_stop_traff_graph.update_yaxes(tickformat=",.0f")
        cust_stop_traff_graph.update_xaxes(showgrid=False)
        cust_stop_traff_graph.update_yaxes(showgrid=False)
        cust_stop_traff_graph.update_yaxes(zeroline=False)
        st.plotly_chart(cust_stop_traff_graph)

        # ax.set_ylabel('Average Traffic')
        # ax.set_title('Customer and Stop Traffic by Day of the Week')
        # ax.set_xlabel('Day of the Week')
        # ax.legend()
        # st.pyplot(fig)
        
    else:
        st.info("Please upload an Excel file on the Home page to get started")
