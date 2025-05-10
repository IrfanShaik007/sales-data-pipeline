from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import snowflake.connector
import random
import json
from faker import Faker
from airflow.operators.bash import BashOperator


# Default args for both tasks
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Fake data setup
fake = Faker()

products = [
    {"product_id": "P1001", "name": "Bluetooth Headphones", "category": "Electronics", "price": 49.99},
    {"product_id": "P1002", "name": "Yoga Mat", "category": "Fitness", "price": 20.00},
    {"product_id": "P1003", "name": "Laptop Stand", "category": "Office", "price": 35.00},
    {"product_id": "P1004", "name": "Water Bottle", "category": "Fitness", "price": 15.00},
    {"product_id": "P1005", "name": "LED Monitor", "category": "Electronics", "price": 120.00}
]

# Function to generate sales data
def generate_sales_data(**kwargs):
    sales = []
    for i in range(1000):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        sale = {
            "sale_id": f"S{1000 + i}",
            "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "quantity": quantity,
            "total_price": round(product["price"] * quantity, 2),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat()
        }
        sales.append(sale)

    with open("/opt/airflow/data/sales_data.json", "w") as f:
        json.dump(sales, f, indent=2)

    print("✅ 1000 sales records written to sales_data.json")

# Function to load sales data to Snowflake
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

# Define the DAG
with DAG('sales_data_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    # Task to generate sales data
    generate_data = PythonOperator(
        task_id='generate_sales_jsonmix',
        python_callable=generate_sales_data
    )

    # Task to load sales data to Snowflake
    load_data = PythonOperator(
        task_id='load_sales_to_snowflakemix',
        python_callable=sales_to_snowflake
    )


    run_dbt_transform = BashOperator(
    task_id='run_dbt_transform',
    bash_command='cd /opt/airflow/dbt/sales_analysis && dbt run',
    dag=dag
)



    # Define task dependencies
    generate_data >> load_data >> run_dbt_transform
