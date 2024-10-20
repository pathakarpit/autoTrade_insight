import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import psycopg2
import json

#below function retrieves data from API
def get_old_data(search_symbol):
    today = datetime.now()
    old = today - timedelta(days=15)
    start_date = old.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    stock_data = yf.download(search_symbol, start = start_date, end = end_date).reset_index()
    return stock_data

#extracting credentials and connecting to psql server
with open('sql_cred.json') as f:
    credentials = json.load(f)

connection = psycopg2.connect(
    dbname=credentials['dbname'],
    user=credentials['user'],
    password=credentials['password'],
    host=credentials['host'],
    port=credentials['port']
)
cursor = connection.cursor()

#reading the stock lists
stock_list = pd.read_csv('Stocks_list.csv')
stock_list['search_symbol'] = stock_list.apply(lambda row: row['stock_symbol'] + ('.NS' if row['exchange'] == 'NSE' else '.BO'), axis=1)

#creating table in db if it doesnt exist already
create_stock_list_table = f"""
CREATE TABLE IF NOT EXISTS "stock_list"(
    stock_name VARCHAR(70),
    stock_symbol VARCHAR(15),
    exchange VARCHAR(5),
    sector VARCHAR(30),
    UNIQUE (stock_symbol)
    );
"""
cursor.execute(create_stock_list_table)
#filling up values in the stocks list table
for index, row in stock_list.iterrows():
    insert_query = f"""
        INSERT INTO "stock_list" (stock_name,stock_symbol, exchange, sector)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (stock_symbol) DO NOTHING;  -- Avoid inserting duplicates
        """
    cursor.execute(insert_query, (row['stock_name'], row['stock_symbol'], row['exchange'], row['sector']))

#creating fin table for each stock
for index, row in stock_list.iterrows():
    stock_symbol = row.iloc[1]
    search_symbol = row.iloc[4]
    create_relevant_table = f"""
    CREATE TABLE IF NOT EXISTS "{str(stock_symbol)}_fin" (
        date DATE,
        symbol VARCHAR(20),
        open DECIMAL(10, 2),
        high DECIMAL(10, 2),
        low DECIMAL(10, 2),
        close DECIMAL(10, 2),
        adj_close DECIMAL(10, 2),
        volume BIGINT,
        UNIQUE (date)
    );
    """
    #filling up table with stock values day wise
    cursor.execute(create_relevant_table)
    data = get_old_data(search_symbol)
    for index, row in data.iterrows():
        insert_query = f"""
        INSERT INTO "{str(stock_symbol)}_fin" (date,symbol, open, high, low, close, adj_close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;  -- Avoid inserting duplicates
        """
        cursor.execute(insert_query, (row['Date'],stock_symbol, row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))

#commiting changes to db and closing connection    
connection.commit()
cursor.close()
connection.close()