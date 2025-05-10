import json 

with open('sales_data.json',"r") as f:
    data=json.load(f)

print(json.dumps(data,indent=2))





