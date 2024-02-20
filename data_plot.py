import pandas as pd 
import plotly.express as px




def plot_bar_chart(df, name):
    
    fig = px.bar(df, df[name].value_counts().index, df[name].value_counts().values, color=df[name].value_counts().index)

    return fig 

def plot_pie_chart(df, name):
    fig = px.pie(df, df[name].value_counts().index, df[name].value_counts().values, hole=.1)
    return fig


def funnel_chart(df, name):
    fig = px.funnel_area(df, df[name].value_counts().index, df[name].value_counts().values)
    return fig 


def plot_day_register(df, name):

    if df[name].dtype != 'datetime64[ns]':
        
        df[name] = pd.to_datetime(df[name])
        df[name] = df[name].dt.date

        registers_by_date = df.groupby(name).size().reset_index(name='Registros')

        fig = px.line(registers_by_date, x=name, y='Registros')

    return fig 


def plot_weekly_register(df, name):
    # Ensure the column is in datetime format
    if df[name].dtype != 'datetime64[ns]':
        df[name] = pd.to_datetime(df[name])

    # Set the datetime column as the index
    df = df.set_index(name)

    # Resample the DataFrame by week and count the number of records in each week
    weekly_counts = df.resample('W').size().reset_index(name='Registros')

    # Reset the index to turn the datetime index back into a regular column
    weekly_counts[name] = weekly_counts[name].dt.date

    # Plot the data
    fig = px.line(weekly_counts, x=name, y='Registros')

    return fig