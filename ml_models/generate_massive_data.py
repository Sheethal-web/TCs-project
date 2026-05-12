import json
import random
from datetime import datetime, timedelta
import os
import re

print("--- INITIALIZING HUGE DATA GENERATOR (1 MILLION ROWS / 200 ITEMS) ---")

# Load the 200 items from the JS file
js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'data', 'products.js')
with open(js_path, 'r') as f:
    js_content = f.read()

# Extract JSON array
json_str = js_content[js_content.find('['):js_content.rfind(']')+1]
products_list = json.loads(json_str)

ALL_ITEMS = [(p['name'], p['price'], p['category']) for p in products_list]
ITEM_NAMES = [p['name'] for p in products_list]

# Complex Hidden Patterns (Bundles) out of 200 items
BUNDLES = {
    'Smartphone': 'Wireless Earbuds',
    'Laptop': 'External SSD',
    '4K TV': 'Soundbar',
    'Gaming Console': 'Gaming Mouse',
    'Eggs': 'Bread',
    'Pasta': 'Tomato Sauce',
    'Tortilla Chips': 'Salsa',
    'Coffee Beans': 'Coffee Maker',
    'Shampoo': 'Conditioner',
    'Toothbrush': 'Toothpaste',
    'Dress Shoes': 'Socks',
    'Notebook': 'Pens',
    'Hammer': 'Nails',
    'Flashlight': 'Batteries (AA)',
    'Dog Food': 'Dog Treats',
    'Cat Litter': 'Cat Food'
}

num_rows = 1000000  # 1 MILLION ROWS
batch_size = 100000

output_file = os.path.join(os.path.dirname(__file__), 'massive_sales_data.csv')

with open(output_file, 'w') as f:
    f.write("Transaction_ID,Date,Time,Product_Name,Category,Price,Quantity,Total_Sales,Is_Bundle_Triggered\n")

start_date = datetime(2023, 1, 1)
transaction_id = 100000
total_generated = 0

print(f"Writing directly to {output_file} in chunks to save memory...")

for batch in range(num_rows // batch_size):
    rows = []
    for _ in range(batch_size):
        days_offset = random.randint(0, 1095) 
        tx_date = start_date + timedelta(days=days_offset)
        hour = random.randint(9, 21)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        date_str = tx_date.strftime("%Y-%m-%d")

        # Cart logic
        cart_size = random.randint(1, 6) # slightly larger carts
        selected_items = random.sample(ALL_ITEMS, cart_size)
        
        # Bundle logic injection
        added_bundles = []
        is_bundle = "No"
        for item in selected_items:
            name, price, cat = item
            if name in BUNDLES and random.random() < 0.65: # 65% chance to trigger bundle
                bundle_item_name = BUNDLES[name]
                # Find bundle item tuple
                bundle_tuple = next(i for i in ALL_ITEMS if i[0] == bundle_item_name)
                added_bundles.append(bundle_tuple)
                is_bundle = "Yes"
                
        final_cart = selected_items + added_bundles
        # Remove duplicates
        final_cart = list(set(final_cart))
        
        for name, price, cat in final_cart:
            qty = random.randint(1, 3)
            total = price * qty
            rows.append(f"{transaction_id},{date_str},{time_str},{name},{cat},{price},{qty},{total},{is_bundle}\n")
            
        transaction_id += 1

    with open(output_file, 'a') as f:
        f.writelines(rows)
        
    total_generated += batch_size
    print(f"Generated {total_generated:,} / {num_rows:,} base transactions...")

print("\n✅ MASSIVE DATASET GENERATION COMPLETE!")
