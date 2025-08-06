"""
bank_project.py
This module implements an ETL (Extract, Transform, Load) pipeline for scraping, transforming, 
and storing bank market capitalization data from a specified website. The pipeline extracts 
data from a web page, transforms it using currency exchange rates, and loads the results 
into both a CSV file and a SQLite database. It also provides functionality to run queries 
on the resulting database.
Functions:
    extract(url, table_attribs): 
        Extracts bank data from the specified URL and returns it as a pandas DataFrame.
    transform(df, csv_path): 
        Transforms the DataFrame by converting market capitalization values to multiple 
        currencies using exchange rates from a CSV file.
    load_to_csv(df, output_path): 
        Saves the DataFrame to a CSV file at the specified path.
    load_to_db(df, sql_connection, table_name): 
        Loads the DataFrame into a specified table in a SQLite database.
    run_query(query_statement, sql_connection): 
        Executes a SQL query on the database and logs the output.
    run(): 
        Orchestrates the entire ETL process: extraction, transformation, loading, and 
        sample queries.
Dependencies:
    - pandas
    - requests
    - BeautifulSoup (bs4)
    - sqlite3
    - src.logging.logger
    - src.config.config
"""

import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.logging.logger import logger
from src.config.config import BANK_URL, BANK_EXCHANGE_RATE_URL,\
BANK_DB,BANK_TABLE, BANK_SCHEMA, BANK_OUTPUT

def extract(url,table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    page = requests.get(url, timeout=10).text
    data = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    if tables:
        rows = tables[0].find_all('tr')
        logger.info(f"Extracting data from {rows}...")
        for row in rows[1:]:
            cols = row.find_all('td')
            data_dict = {"Name": cols[1].find_all('a')[1].get_text(),
                        "MC_USD_Billion": cols[2].get_text().strip()}
            df.loc[len(df)] = data_dict

    return df

def transform(df,csv_path):
    ''' This function accesses the CSV file BANK_EXCHANGE_RATE_URL for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies.'''
    # Load exchange rate data from BANK_EXCHANGE_RATE_URL url
    exchange_rate_df = pd.read_csv(csv_path)
    # add 3 columns to the dataframe df MC_GBP_Billion, MC_EUR_Billion, MC_INR_Billion
    df["MC_GBP_Billion"] = df["MC_USD_Billion"].astype(float) \
    * exchange_rate_df[exchange_rate_df['Currency'] == 'GBP']['Rate'].values[0]
    df["MC_EUR_Billion"] = df["MC_USD_Billion"].astype(float) \
    * exchange_rate_df[exchange_rate_df['Currency'] == 'EUR']['Rate'].values[0]
    df["MC_INR_Billion"] = df["MC_USD_Billion"].astype(float) \
    * exchange_rate_df[exchange_rate_df['Currency'] == 'INR']['Rate'].values[0]
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path, index=False)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
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
    # Extract data from the website
    logger.info("Extracting data from the website...")
    df = extract(BANK_URL, BANK_SCHEMA)

    # Transform the data
    logger.info("Transforming data...")
    df = transform(df, BANK_EXCHANGE_RATE_URL)

    # Load the data to a CSV file
    logger.info(f"Loading data to CSV file: {BANK_OUTPUT}")
    load_to_csv(df, BANK_OUTPUT)

    # Load the data to a database
    logger.info(f"Loading data to database table: {BANK_TABLE}")
    sql_connection = sqlite3.connect(BANK_DB)
    load_to_db(df, sql_connection, BANK_TABLE)

    # Run a sample query on the database table
    logger.info("Running sample query on the database table...")
    query_statement = f"SELECT * FROM {BANK_TABLE}"
    run_query(query_statement, sql_connection)
    query_statement = f"SELECT AVG(MC_GBP_Billion) FROM {BANK_TABLE}"
    run_query(query_statement, sql_connection)
    query_statement = f"SELECT Name FROM {BANK_TABLE} LIMIT 5"
    run_query(query_statement, sql_connection)

    # Close the database connection
    sql_connection.close()
    logger.info("ETL process completed successfully.")
    print("ETL process completed successfully.")
