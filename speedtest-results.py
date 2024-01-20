#!/usr/bin/env python3
#
# Created by RejectH0 - 19 JAN 2024 - 1924 MST
#
import configparser
import pymysql
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from icecream import ic

# Configuration Variables
config = configparser.ConfigParser()
config.read('config.ini')
DB_HOST = config['database']['host']
DB_PORT = int(config['database']['port'])
DB_USER = config['database']['user']
DB_PASS = config['database']['password']

def get_databases(cursor):
    try:
        cursor.execute("SHOW DATABASES;")
        all_dbs = cursor.fetchall()
        speedtest_dbs = [db[0] for db in all_dbs if db[0].endswith('-speedtest')]
        ic("Databases found:", speedtest_dbs)  # Debugging line
        return speedtest_dbs
    except Exception as e:
        ic(f"Error fetching database list: {e}")
        return []

def fetch_data(cursor, db_name):
    try:
        query = """
        SELECT timestamp, (download / 1024 / 1024) AS download_mbps, (upload / 1024 / 1024) AS upload_mbps FROM {}
        """.format(db_name + ".speedtest_results")
        cursor.execute(query)
        ic("Data from", db_name, ":", data.head())
        return pd.DataFrame(cursor.fetchall(), columns=['timestamp', 'download_mbps', 'upload_mbps'])
    except Exception as e:
        ic(f"Error fetching data from database {db_name}: {e}")
        return pd.DataFrame()

def plot_data(data, db_name):
    try:
        ic("Plotting data for", db_name)
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        plt.plot(data['timestamp'], data['download_mbps'], label='Download Mbps', color='blue')
        plt.plot(data['timestamp'], data['upload_mbps'], label='Upload Mbps', color='red')
        plt.xlabel('Timestamp')
        plt.ylabel('Speed (Mbps)')
        plt.title(f'Speedtest Results for {db_name}')
        plt.legend()
        # Filename for the output PNG
        filename = f'{db_name}_speedtest_results.png'
        ic(f"Creating plot for {db_name}, saving as {filename}")

        # Saving the plot as a PNG file
        plt.savefig(filename)
        ic(f"Plot saved as {filename}")

        plt.close()
    except Exception as e:
        ic(f"Error plotting data for database {db_name}: {e}")

def main():
    conn = None
    try:
        # Connect to MariaDB
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS)
        cursor = conn.cursor()

        # Retrieve list of databases
        dbs = get_databases(cursor)
        ic("Databses Found: ",dbs)
        
        for db in dbs:
            # Fetch data from each database
            data = fetch_data(cursor, db)

            # Plot the data if there is data to plot
            if not data.empty:
                plot_data(data, db)

    except Exception as e:
        ic(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
