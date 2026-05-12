import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

print("--- INITIALIZING MASSIVE DATA GENERATOR (1 MILLION ROWS) ---")
print("This will simulate 3 years of enterprise-scale transaction data...")

# Categories & Products
PRODUCTS = {
    'Electronics & Tech': [
        ('Laptop', 45000), ('Wireless Mouse', 1200), ('DSLR Camera', 55000), 
        ('SD Card', 800), ('Smart TV', 35000), ('Soundbar', 8000)
    ],
    'Food & Restaurant': [
        ('Pasta', 250), ('Garlic Bread', 100), ('Burger', 150), 
        ('Large Fries', 80), ('Mutton Curry', 450), ('Cold Coffee', 120)
    ],
    'Parents & Baby': [
        ('Diapers', 600), ('Wet Wipes', 150), ('Baby Lotion', 350), 
        ('Baby Wash', 300), ('Stroller', 4500), ('Baby Monitor', 2500)
    ],
    'School & Education': [
        ('Notebooks (Set of 5)', 300), ('Blue Pens', 50), ('Backpack', 800), 
        ('Lunch Box', 400), ('Scientific Calculator', 900)
    ]
}

# Flatten for easy random selection
ALL_ITEMS = []
for cat, items in PRODUCTS.items():
    for name, price in items:
        ALL_ITEMS.append((name, price, cat))

# AI Hidden Patterns (Bundles)
BUNDLES = {
    'Laptop': 'Wireless Mouse',
    'DSLR Camera': 'SD Card',
    'Pasta': 'Garlic Bread',
    'Burger': 'Large Fries',
    'Diapers': 'Wet Wipes',
    'Notebooks (Set of 5)': 'Blue Pens'
}

num_rows = 1000000  # 1 MILLION ROWS!
batch_size = 100000

output_file = os.path.join(os.path.dirname(__file__), 'massive_sales_data.csv')

# Write header
with open(output_file, 'w') as f:
    f.write("Transaction_ID,Date,Time,Product_Name,Category,Price,Quantity,Total_Sales,Is_Bundle_Triggered\n")

start_date = datetime(2023, 1, 1)

transaction_id = 100000
total_generated = 0

print(f"Writing directly to {output_file} in chunks to save memory...")

for batch in range(num_rows // batch_size):
    rows = []
    for _ in range(batch_size):
        # Time generation
        days_offset = random.randint(0, 1095) # 3 years
        tx_date = start_date + timedelta(days=days_offset)
        
        # Peak hours simulation (12 PM - 2 PM, 6 PM - 8 PM)
        if random.random() < 0.4:
            hour = random.choice([12, 13, 18, 19])
        else:
            hour = random.randint(9, 21)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        date_str = tx_date.strftime("%Y-%m-%d")

        # Cart logic
        cart_size = random.randint(1, 4)
        selected_items = random.sample(ALL_ITEMS, cart_size)
        
        # Bundle logic injection
        added_bundles = []
        is_bundle = "No"
        for item in selected_items:
            name, price, cat = item
            if name in BUNDLES and random.random() < 0.75: # 75% chance to buy bundle
                bundle_item_name = BUNDLES[name]
                # Find bundle item tuple
                bundle_tuple = next(i for i in ALL_ITEMS if i[0] == bundle_item_name)
                added_bundles.append(bundle_tuple)
                is_bundle = "Yes"
                
        # Merge cart
        final_cart = selected_items + added_bundles
        
        for name, price, cat in final_cart:
            qty = random.randint(1, 2)
            if price > 10000: qty = 1 # Expensive items are rarely bought in bulk
            
            total = price * qty
            rows.append(f"{transaction_id},{date_str},{time_str},{name},{cat},{price},{qty},{total},{is_bundle}\n")
            
        transaction_id += 1

    # Append to file
    with open(output_file, 'a') as f:
        f.writelines(rows)
        
    total_generated += batch_size
    print(f"Generated {total_generated:,} / {num_rows:,} base transactions...")

print("\n✅ MASSIVE DATASET GENERATION COMPLETE!")
print(f"File saved to: {output_file}")
print(f"Size: ~{os.path.getsize(output_file) / (1024 * 1024):.2f} MB")
print("You can now import this 1-Million-Row CSV into Pandas, AWS S3, Tableau, or train Deep Learning models on it!")
