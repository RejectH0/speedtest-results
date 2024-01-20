#!/usr/bin/env python3
#
# Created by RejectH0 - 19 JAN 2024 - 1945 MST
#
import configparser
import pymysql
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
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
        speedtest_dbs = [db[0] for db in all_dbs if db[0].endswith('_speedtest')]
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
        data = pd.DataFrame(cursor.fetchall(), columns=['timestamp', 'download_mbps', 'upload_mbps'])
        ic("Data from", db_name, ":", data.head())  # Moved this line here
        return data
    except Exception as e:
        ic(f"Error fetching data from database {db_name}: {e}")
        return pd.DataFrame()

def plot_data(data, db_name):
    try:
        # Convert 'timestamp' column to datetime objects
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        sns.set(style="whitegrid")
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('Download Speed (Mbps)', color=color)
        ax1.plot(data['timestamp'], data['download_mbps'], label='Download Mbps', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Set the y-axis for download to show full range of data
        ax1.set_ylim(min(data['download_mbps']) - (max(data['download_mbps']) * 0.1), 
                     max(data['download_mbps']) + (max(data['download_mbps']) * 0.1))

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:red'
        ax2.set_ylabel('Upload Speed (Mbps)', color=color)  
        ax2.plot(data['timestamp'], data['upload_mbps'], label='Upload Mbps', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Set the y-axis for upload to show full range of data
        ax2.set_ylim(min(data['upload_mbps']) - (max(data['upload_mbps']) * 0.1), 
                     max(data['upload_mbps']) + (max(data['upload_mbps']) * 0.1))

        # Improve the readability of the x-axis.
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        fig.autofmt_xdate()  # Rotation

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(f'Speedtest Results for {db_name}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Generate the filename with the current date and time
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{db_name}-{current_time}.png"
        ic(f"Creating plot for {db_name}, saving as {filename}")

        # Save the plot as a PNG file
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
