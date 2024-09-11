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
# Getting input from user
col1, col2 = st.columns([1, 1])
with col1:
    stock_list = st.multiselect("Choose 4 stocks",
                                ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
                                ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
with col2:
    year = st.number_input("Number of years", 1, 10)
# Downloading data for SP500
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    SP500 = web.DataReader(['sp500'], 'fred', start, end)

    stocks_df = pd.DataFrame()
    for stock in stock_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].apply(lambda x: str(x)[:10]))
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.plotly_chart(interactive_plot(normalize(stocks_df)))

    stocks_daily_return = daily_return(stocks_df)

    beta = {}
    alpha = {}
    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame({'Stock': beta.keys(), 'Beta Value': [str(round(b, 2)) for b in beta.values()]})
    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df, use_container_width=True)

    rf = 0  # Risk-free rate
    rm = stocks_daily_return['sp500'].mean() * 252  # Market return

    return_df = pd.DataFrame()
    return_df['Stock'] = stock_list
    return_df['Return Value'] = [str(round(rf + (beta[stock] * (rm - rf)), 2)) for stock in stock_list]

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

except Exception as e:
    st.write("Error:", str(e))
"""

with open('app.py', 'w') as f:
    f.write(code)

!streamlit run app.py &>/dev/null&
!npx localtunnel --port 8501
