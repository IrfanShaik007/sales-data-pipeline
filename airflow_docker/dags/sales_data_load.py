from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import snowflake.connector

def sales_to_snowflake():
    df = pd.read_json("/opt/airflow/data/sales_data.json")

    # Convert timestamp string to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    conn = snowflake.connector.connect(
        user='IRFAN',
        password='Irfanshareef007',
        account='SUBLRSH-DN43695',
        warehouse='COMPUTE_WH',
        database='SALES_ANALYTICS',
        schema='RAW'
    )
    cursor = conn.cursor()

    for _, row in df.iterrows():
        # Convert the timestamp to string in the required format
        timestamp_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(
            "INSERT INTO RAW_SALES_DATA(sale_id, product_id, product_name, category, price, quantity, total_price, timestamp) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (row['sale_id'], row['product_id'], row['product_name'], row['category'], row['price'], 
             row['quantity'], row['total_price'], timestamp_str)  # Use string here
        )

    conn.commit()
    cursor.close()
    conn.close()


default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG('sales_data_load',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    task = PythonOperator(
        task_id='load_sales_to_snowflake',
        python_callable=sales_to_snowflake
    )
    