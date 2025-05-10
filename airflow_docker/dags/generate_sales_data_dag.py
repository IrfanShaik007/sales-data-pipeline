from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import random
from faker import Faker

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

fake = Faker()

products = [
    {"product_id": "P1001", "name": "Bluetooth Headphones", "category": "Electronics", "price": 49.99},
    {"product_id": "P1002", "name": "Yoga Mat", "category": "Fitness", "price": 20.00},
    {"product_id": "P1003", "name": "Laptop Stand", "category": "Office", "price": 35.00},
    {"product_id": "P1004", "name": "Water Bottle", "category": "Fitness", "price": 15.00},
    {"product_id": "P1005", "name": "LED Monitor", "category": "Electronics", "price": 120.00}
]

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

with DAG(
    dag_id='generate_sales_data',
    default_args=default_args,
    schedule_interval='@daily',  # or '@once' for testing
    catchup=False,
    tags=['data-generator']
) as dag:

    generate_data = PythonOperator(
        task_id='generate_sales_json',
        python_callable=generate_sales_data
    )
