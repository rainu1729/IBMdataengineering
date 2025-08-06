import pandas as pd 
import requests
from bs4 import BeautifulSoup
from src.logging.logger import logger
import sqlite3
import numpy as np


def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path, index=False)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    logger.info(f"query statement: {query_statement}")
    query_output = pd.read_sql(query_statement, sql_connection)
    logger.info(f"query output: {query_output}")


def run():
    ''' This function runs the entire ETL pipeline. It extracts the
    data from the website, transforms it, loads it to a CSV file and
    a database table. It also runs a sample query on the database table.'''
    
    # Load environment variables
    from src.config.config import GDP_DATA_URL, GDP_DATA_DB, GDP_DATA_TABLE, GDP_DATA_SCHEMA , GDP_DATA_OUTPUT
    
    # Extract
    logger.info(f"Starting data extraction from URL: {GDP_DATA_URL}")
    df = extract(GDP_DATA_URL, GDP_DATA_SCHEMA)
    
    # Transform
    logger.info("Starting data transformation...")
    if df.empty:
        logger.error("No data extracted. Exiting ETL process.")
        return  
    df = transform(df)
    
    # Load to CSV
    logger.info(f"Loading data to CSV file: {GDP_DATA_OUTPUT}")
    if not df.empty:
        load_to_csv(df, GDP_DATA_OUTPUT)
    else:
        logger.error("DataFrame is empty. No CSV file created.")
    
    
    # Load to DB
    logger.info("Create db connection")
    sql_connection = sqlite3.connect(GDP_DATA_DB)

    logger.info("load data into database")
    load_to_db(df, sql_connection, GDP_DATA_TABLE)

    logger.info("frame query to execute")
    query_statement = f"SELECT * from {GDP_DATA_TABLE} where GDP_USD_billions >=100"

    logger.info("call run_query function")
    run_query(query_statement,sql_connection)

    sql_connection.close()

    logger.info('Process completed')
  