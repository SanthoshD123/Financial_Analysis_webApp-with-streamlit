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
import plotly.express as px"""
