import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go

# Useful functions
def color_hr(val, hour=20):
    color = 'green' if val >= hour else 'red'
    return f'background-color: {color}'

def app():
    st.title('Members Dashboard 👩‍💼👨‍💼')

    member_example = "data\member_example.png"

    with st.expander('Help ✋'):
        st.markdown('***How does this work?***')
        st.markdown('This dashboard will automatically load all the data from the "Member Actions" sheet in the Excel file you upload. It will then provide summary tables and insightful visualizations of the data. The first table will showcase each member\'s number of hours worked. The right column will be displayed as green if the individual member worked at least 40 hours or red if the individual member worked less than 40 hours. Explore individual work contributions by selecting a "Member Name" for the next two tables.')
        st.markdown('***Why am I getting an error?***')
        st.markdown('If you are getting an error, please make sure that you are uploading the correct file. The file should be an excel file with a sheet named "Member Actions".')
        st.markdown('Within the "Member Actions" sheet, there should be these four columns: Date, Member Name, Task, and Duration. You can add columns to the sheet, but you must have at least the specified columns.')
        st.image(member_example, caption = 'Example')

    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file

        st.markdown('Note: To accurately track time on this dashboard, please input durations in hours. For instances where work spans less than an hour, use decimal values. For example, if Joe worked for one hour and thirty minutes, he would input 1.5.')

        # df = pd.read_excel(uploaded_file, sheet_name=['Member Actions'])
        dataframe = pd.read_excel(uploaded_file, sheet_name=['Member Actions'])
        df = dataframe['Member Actions']
        # df_details = df['Member Actions']
        df_summary = df[['Member Name', 'Duration']].groupby('Member Name')['Duration'].sum().reset_index()  
        df_summary_styled = df_summary.style.applymap(color_hr, subset=['Duration'])

        # # Display the styled dataframe
        # st.dataframe(df_summary_styled)
        # Display summary table
        st.subheader("Member Actions")
        st.dataframe(df)
        st.header("Summary of Hours Worked")
        st.dataframe(df_summary_styled)

        st.header("Select Member")
        gb_summary = GridOptionsBuilder.from_dataframe(df_summary)
        gb_summary.configure_default_column(editable=False, groupable=True)
        gb_summary.configure_selection('single', use_checkbox=True)
        gridOptions_summary = gb_summary.build()

        summary_response = AgGrid(
            df_summary,
            gridOptions=gridOptions_summary,
            enable_enterprise_modules=False,
            editable=False,
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme='streamlit',
            height=200,
            width='100%'
        )

        # Debugging: Print the selected rows and its type
        st.write("Selected Rows Debug Info:")
        st.write(summary_response['selected_rows'])
        # st.write("Type of selected rows:")
        # st.write(type(summary_response['selected_rows']))

        # Get selected person
        try:
            selected = summary_response['selected_rows']

            if not selected.empty:
                selected_name = selected.iloc[0]['Member Name']
                st.write(f"Tasks for {selected_name}:")
                df_selected_details = df[df['Member Name'] == selected_name]
                gb_details = GridOptionsBuilder.from_dataframe(df_selected_details)
                gb_details.configure_default_column(editable=False, groupable=True)
                gridOptions_details = gb_details.build()

                details_response = AgGrid(
                    df_selected_details,
                    gridOptions=gridOptions_details,
                    enable_enterprise_modules=False,
                    editable=False,
                    fit_columns_on_grid_load=True,
                    update_mode=GridUpdateMode.NO_UPDATE,
                    theme='streamlit',
                    height=200,
                    width='100%'
                )
            else:
                st.write("No selection made. Please select a row to see task details.")
        except:
            st.write("No selection made. Please select a row to see task details.")


        st.subheader("Total Duration by Member Name")
        members_graph = go.Figure()

        members_graph.add_trace(go.Bar(
            x=df_summary['Member Name'],
            y=df_summary['Duration'],
            marker_color='#F63366', 
            hovertemplate='Member: %{x}<br>Duration: %{y} Hours</b><extra></extra>'
        ))

        members_graph.add_shape(
            type='line',
            x0=-0.6, x1=len(df_summary),
            y0=40, y1=40,
            line_color='black',
            line_dash='dash',
            line_width=2
        )

        members_graph.update_layout(
            xaxis_title='Member Name',
            yaxis_title='Total Duration (Hours)',
            xaxis_tickangle=45
        )

            # Add annotation (text)
        members_graph.add_annotation(
            x=0.01,
            y=50,
            text='40-Hour<br>Mark',
            showarrow=False,
            font_color='black'
        )

        st.plotly_chart(members_graph)
        # fig, ax = plt.subplots(figsize=(10, 6))
        # ax.bar(df_summary['Member Name'], df_summary['Duration'], color='skyblue')
        # ax.axhline(y=40, color='r', linestyle='--', linewidth=2)
        # ax.set_xlabel('Member Name')
        # ax.set_ylabel('Total Duration')
        # ax.text(0, 42, '40-hour mark', color='red')
        # plt.xticks(rotation=45)
        # plt.tight_layout()

        # st.pyplot(fig)

    else:
        st.info("Please upload an Excel file on the Home page to get started")
