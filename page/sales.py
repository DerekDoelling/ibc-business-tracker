import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Page title
# st.set_page_config(page_title='Sales Dashboard', page_icon='📊')

def app():

    st.title('Sales Dashboard 💰')
    
    sales_example = "C:\\Users\\derek\\OneDrive - BYU-Idaho\\Documents\\Data Science Society\\ibc-business-tracker\\data\\sales_example.png"

    with st.expander('Help ✋'):
        st.markdown('***How does this work?***')
        st.markdown('This dashboard will automatically load all the data from the "Sales" sheet in the Excel file you upload. It will then provide a summary table and insightful visualizations of the data. You can also filter the data by the items sold on the left under ***Filters*** to get a deeper understanding.')
        st.markdown('***Why am I getting an error?***')
        st.markdown('If you are getting an error, please make sure that you are uploading the correct file. The file should be an excel file with a sheet named "Sales".')
        st.markdown('Within the "Sales" sheet, there should be these five columns: Transaction ID, Date, Item Sold, Quantity Sold, and Total Sales. You can add columns to the sheet, but you must have at least the specified columns.')
        st.image(sales_example, caption = 'Example')
    
    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        
        # Load data
        dataframe = pd.read_excel(uploaded_file, sheet_name=['Sales'])
        df = dataframe['Sales']
        
        st.write("This dashboard provides a comprehensive analysis of sales and quantity data over specified dates. Each chart offers insights into different aspects of the data, helping you to understand the patterns and trends. The filter is on the far lefthand side of the screen.")
        
        st.write(f"Summary of the dashboard:  \n- First table is the raw data from the Sales sheet   \n- The following charts give insights into what items are the most popular and profitable. This can help workers to be more effective with inventory. As well as be able to forecast future profits and risks.")
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sidebar filters
        st.sidebar.header('Filters')
        date_range = st.sidebar.date_input('Date range', value=[df['Date'].min().date(), df['Date'].max().date()])
        items = st.sidebar.multiselect('Select Items Sold', options=df['Item Sold'].unique(), default=df['Item Sold'].unique())
        
        # Convert date_range to datetime
        date_range = [pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])]
        
        # Filter data
        filtered_data = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
        if items:
            filtered_data = filtered_data[filtered_data['Item Sold'].isin(items)]
        
        # Display data
        st.subheader('Sales')

        st.dataframe(df)

        # Display overview
        st.header('Sales and Quantity Sold Overview')

        overview = df.copy()
        overview = overview.drop(columns = 'Date')
        overview = overview.groupby('Item Sold')
        overview = overview.describe()
        st.table(overview)
        
        # def plot_line_chart(df, title):
        #         plt.figure(figsize=(10, 6))
        #         sns.lineplot(data=df, x=df["Date"], y=df["Total Sales"])
        #         plt.title(title)
        #         plt.xlabel('Date')
        #         plt.ylabel('Total Sales')
        #         plt.xticks(rotation=45)
        #         st.pyplot(plt)
        
        # plot_line_chart(df,'Sales by Date')
        
        # Sales by Date (Line Chart)
        # st.header("Sales Analysis")

        st.header('Sales by Date')
        sales_by_date = filtered_data.copy()
        sales_by_date['date'] = sales_by_date['Date'].dt.strftime('%b %d')
        sales_by_date = sales_by_date.groupby(['Date', 'date'])['Total Sales'].sum()
        sales_by_date = sales_by_date.reset_index().drop(columns=['Date'])
        sales_by_date = px.line(sales_by_date, x=sales_by_date['date'], y=sales_by_date['Total Sales'], markers=True, color_discrete_sequence=['#F63366'])
        sales_by_date.update_layout(xaxis_title = '',yaxis_title='Total Sales')
        sales_by_date.update_traces(hovertemplate='Date: %{x}<br>Total Sales: <b>$%{y:,.2f}<b><extra></extra>')
        sales_by_date.update_yaxes(tickformat="$.0f")
        sales_by_date.update_layout(xaxis=dict(tickmode='linear',dtick=7))
        sales_by_date.update_xaxes(showgrid=False)
        sales_by_date.update_yaxes(showgrid=False)
        sales_by_date.update_yaxes(zeroline=False)
 
        st.plotly_chart(sales_by_date)
        # fig, ax = plt.subplots()
        # ax.plot(sales_by_date.index, sales_by_date.values, marker='o')
        # ax.set_xlabel('Date')
        # ax.set_ylabel('Total Sales')
        # # ax.set_title('Sales by Date')
        # ax.tick_params(axis='x', rotation=45)  # Make x-axis labels horizontal
        # st.pyplot(fig)
        
        # Sales by Item Sold (Bar Chart)

        st.header('Sales by Day of the Week')
        weekday = filtered_data.copy()
        weekday['DayOfWeek'] = weekday['Date'].dt.day_name()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Filter for weekdays (Monday to Friday)
        weekday_data = weekday[weekday['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        weekday_data['DayOfWeek'] = pd.Categorical(weekday_data['DayOfWeek'], categories=weekday_order, ordered=True)
        weekday_data_sales = weekday_data.groupby('DayOfWeek')['Total Sales'].mean().reset_index()
        weekday_data_sales_graph = px.line(weekday_data_sales, x='DayOfWeek', y='Total Sales', markers=True, color_discrete_sequence=['#F63366'])
        weekday_data_sales_graph.update_layout(xaxis_title = '',yaxis_title='Average Total Sales')
        weekday_data_sales_graph.update_traces(hovertemplate='Day of the Week: %{x}<br>Average Total Sales: <b>$%{y:,.2f}<b><extra></extra>')
        weekday_data_sales_graph.update_yaxes(tickformat="$.0f")
        weekday_data_sales_graph.update_xaxes(showgrid=False)
        weekday_data_sales_graph.update_yaxes(showgrid=False)
        weekday_data_sales_graph.update_yaxes(zeroline=False)
        st.plotly_chart(weekday_data_sales_graph)

        st.header('Sales by Item')
        sales_by_item = filtered_data.groupby('Item Sold')['Total Sales'].sum().sort_values(ascending=True).reset_index()

        sales_by_item = go.Figure(go.Bar(x=sales_by_item['Total Sales'], y=sales_by_item['Item Sold'], orientation='h', marker =dict(color = '#F63366')))
        sales_by_item.update_traces(hovertemplate='Item: %{y}<br>Total Sales: <b>$%{x:,.2f}<b><extra></extra>')
        sales_by_item.update_layout(xaxis_title='Total Sales')
        sales_by_item.update_xaxes(tickformat="$.0f")
        sales_by_item.update_xaxes(showgrid=False)
        sales_by_item.update_yaxes(showgrid=False)
        sales_by_item.update_yaxes(zeroline=False)
        st.plotly_chart(sales_by_item)
        # fig, ax = plt.subplots()
        # sales_by_item.plot(kind='barh', ax=ax)
        # ax.set_ylabel('')
        # ax.set_xlabel('Total Sales $')
        # # ax.set_title('Sales by Item Sold')
        # st.pyplot(fig)
        
        # Quantity Sold by Item Sold (Horizontal Bar Chart)
        st.header('Quantity Sold by Item')
        quantity_by_item = filtered_data.groupby('Item Sold')['Quantity Sold '].sum().sort_values(ascending=True).reset_index()
        quantity_by_item = go.Figure(go.Bar(x=quantity_by_item['Quantity Sold '], y=quantity_by_item['Item Sold'], orientation='h', marker =dict(color = '#F63366')))
        quantity_by_item.update_traces(hovertemplate='Item: %{y}<br>Total Quantity Sold: <b>%{x}<b><extra></extra>')
        quantity_by_item.update_layout(xaxis_title='Total Quantity Sold')
        quantity_by_item.update_xaxes(showgrid=False)
        quantity_by_item.update_yaxes(showgrid=False)
        quantity_by_item.update_yaxes(zeroline=False)
        # fig, ax = plt.subplots()
        # quantity_by_item.plot(kind='barh', ax=ax)
        # ax.set_xlabel('Quantity Sold')
        # ax.set_ylabel('')
        # ax.set_title('Quantity Sold by Item Sold')
        st.plotly_chart(quantity_by_item)
        
        # Extract day of the week
        st.header('Quantity Sold by Day of the Week')
        weekday = filtered_data.copy()
        weekday['DayOfWeek'] = weekday['Date'].dt.day_name()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Filter for weekdays (Monday to Friday)
        weekday_data = weekday[weekday['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        weekday_data['DayOfWeek'] = pd.Categorical(weekday_data['DayOfWeek'], categories=weekday_order, ordered=True)
        weekday_data = weekday_data.groupby(['DayOfWeek', 'Item Sold'])['Quantity Sold '].mean().reset_index()

        quantity_sold = px.line(weekday_data, x=weekday_data['DayOfWeek'], y=weekday_data['Quantity Sold '], color = weekday_data['Item Sold'], markers=True)
        quantity_sold.update_layout(xaxis_title='', yaxis_title='Average Quantity Sold')
        quantity_sold.update_traces(hovertemplate='Item: %{customdata[0]}<br>Day: %{x}<br>Average Quantity Sold: <b>%{y:,.1f}<b><extra></extra>',customdata=weekday_data['Item Sold'].values.reshape(-1, 1))
        quantity_sold.update_xaxes(showgrid=False)
        quantity_sold.update_yaxes(showgrid=False)
        quantity_sold.update_yaxes(zeroline=False)
        st.plotly_chart(quantity_sold)
        # fig, ax = plt.subplots()
        # weekday = weekday.groupby(['DayOfWeek', 'Item'])['Quantity Sold '].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])  #.plot(ax=ax, marker='o', label="")
        
        # weekday_data = px.line(weekday, x=weekday.index, y=weekday['Quantity Sold '], markers=True)
        # weekday_data.update_layout(xaxis_title='Day of the Week', yaxis_title='Average Quantity Sold')
        # weekday_data.update_traces(hovertemplate='Day: %{x}<br>Average Quantity Sold: %{y:.2f}')
        # st.plotly_chart(weekday_data)
        # st.header('Average Quantity Sold by Day of the Week')
        # ax.set_ylabel('Average Quantity Sold')
        # ax.set_title('Average Quantity Sold by Day of the Week')
        # ax.set_xlabel('Day of the Week')
        # ax.legend()
        # st.pyplot(fig)
        
        # Advanced Chart: Pair Plot of Sales Data
        # st.header('Pair Plot of Sales Data')
        # sns.pairplot(df, diag_kind='kde', markers='+')
        # st.pyplot(plt.gcf())
        
    else:
        st.info("Please upload an Excel file on the Home page to get started")
