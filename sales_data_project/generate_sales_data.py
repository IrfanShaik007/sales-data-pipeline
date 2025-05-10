import json
import random
from faker import Faker
from datetime import datetime,timedelta
fake=Faker()

products = [
    {"product_id": "P1001", "name": "Bluetooth Headphones", "category": "Electronics", "price": 49.99},
    {"product_id": "P1002", "name": "Yoga Mat", "category": "Fitness", "price": 20.00},
    {"product_id": "P1003", "name": "Laptop Stand", "category": "Office", "price": 35.00},
    {"product_id": "P1004", "name": "Water Bottle", "category": "Fitness", "price": 15.00},
    {"product_id": "P1005", "name": "LED Monitor", "category": "Electronics", "price":120.00}
]

def generate_sales_data(n):
    sales=[]
    for i in range(n):
        product=random.choice(products)
        quantity=random.randint(1,5)
        sale={
            "sale_id": f"S{1000 + i}",
            "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "quantity":quantity,
            "total_price":round(product["price"]*quantity,2),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat()
        }
        sales.append(sale)
    return sales

def write_to_file(data, filename="sales_data.json"):
    with open(filename,"w") as f:
        json.dump(data,f,indent=2)

if __name__ == "__main__":
    data=generate_sales_data(1000)
    write_to_file(data)
    print("1000 sales records written to sales_data.json")

