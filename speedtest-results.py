#!/usr/bin/env python3
#
# Created by RejectH0 - 19 JAN 2024 - 1530 MST
#
import configparser
import pymysql
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Configuration Variables
config = configparser.ConfigParser()
config.read('config.ini')
DB_HOST = config['database']['host']
DB_PORT = int(config['database']['port'])
DB_USER = config['database']['user']
DB_PASS = config['database']['password']

def get_databases(cursor):
    # Placeholder for fetching database names matching a pattern
    pass

def fetch_data(cursor, db_name):
    # Placeholder for fetching data from a specific database
    pass

def plot_data(data, db_name):
    # Placeholder for plotting data using Seaborn and saving as PNG
    pass

def main():
    try:
        # Connect to MariaDB
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS)
        cursor = conn.cursor()

        # Retrieve list of databases
        dbs = get_databases(cursor)

        for db in dbs:
            # Fetch data from each database
            data = fetch_data(cursor, db)

            # Plot the data
            plot_data(data, db)

    except Exception as e:
        print(f"Error: {e}")
        # Handle other exceptions as necessary
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
