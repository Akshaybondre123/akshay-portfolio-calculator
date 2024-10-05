import json
import os  
import numpy as np  
from utils import apply_fifo, calculate_portfolio_value, xirr


try:
    with open('data/transaction_detail.json', 'r') as f:
        data = json.load(f)
        print(data)  
except FileNotFoundError:
    print("The transaction detail JSON file was not found.")
    exit()
except json.JSONDecodeError:
    print("Error decoding JSON. Please check the file format.")
    exit()

if 'data' not in data or not data['data']:
    print("Invalid JSON structure. Please check the file.")
    exit()


transactions = data['data'][0]['dtSummary']  


folio_units = apply_fifo(transactions)
total_value, total_gain = calculate_portfolio_value(folio_units)


print(f"Total Portfolio Value: {total_value}")
print(f"Total Portfolio Gain: {total_gain}")


output_dir = './output/'
os.makedirs(output_dir, exist_ok=True)  

output_file_path = os.path.join(output_dir, 'portfolio_result.txt')
try:
    with open(output_file_path, 'w') as f:
        f.write(f"Total Portfolio Value: {total_value}\n")
        f.write(f"Total Portfolio Gain: {total_gain}\n")
    print(f"Results successfully written to {output_file_path}.")
except Exception as e:
    print(f"Error writing to file: {e}")


portfolio_xirr = xirr(transactions, total_value)
print(f"Portfolio XIRR: {portfolio_xirr}")
