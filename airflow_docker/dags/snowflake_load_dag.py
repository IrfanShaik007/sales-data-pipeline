from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import snowflake.connector
import os

def load_to_snowflake():
    # Read the CSV
    df = pd.read_csv('/opt/airflow/data/sample_data.csv')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user='IRFAN',
        password='Irfanshareef007',
        account='SUBLRSH-DN43695',
        warehouse='COMPUTE_WH',
        database='SALES_ANALYTICS',
        schema='RAW'
    )
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id INT,
            name STRING,
            amount INT
        )
    """)

    # Insert data
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO my_table (id, name, amount) VALUES (%s, %s, %s)",
            (row['id'], row['name'], row['amount'])
        )

    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG('snowflake_load_dag',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    task = PythonOperator(
        task_id='load_csv_to_snowflake',
        python_callable=load_to_snowflake
    )
