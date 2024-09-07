#Run in colab
!pip install streamlit pandas yfinance pandas_datareader plotly
!npm install -g localtunnel

code = """
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import numpy as np
import plotly.express as px

# Function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig 
# Function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i].iloc[0]
    return df
# Function to calculate daily returns
def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        df_daily_return[i] = df_daily_return[i].pct_change() * 100
    df_daily_return.fillna(0, inplace=True)
    return df_daily_return
# Function to calculate beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a

st.set_page_config(page_title="CAPM", page_icon="📈", layout='wide')

st.title("Capital Asset Pricing Model (CAPM)")
 """
