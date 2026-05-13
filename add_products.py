#!/usr/bin/env python3
import csv
import random

# Read existing products
existing_products = []
with open('ml_models/products.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_products.append({
            'id': int(row['id']),
            'name': row['name'],
            'price': float(row['price']),
            'category': row['category']
        })

# Get unique items from groceries
unique_items = set()
with open('temp_groceries.csv', 'r') as f:
    for line in f:
        items = [item.strip() for item in line.split(',') if item.strip()]
        unique_items.update(items)

# Remove items that are already in products.csv
existing_names = {p['name'].lower() for p in existing_products}
new_items = [item for item in unique_items if item.lower() not in existing_names]

print(f'Adding {len(new_items)} new products')

# Categorize and price the new items
categories = {
    'Dairy': ['butter', 'butter milk', 'cheese', 'cream cheese', 'curd', 'milk', 'whipped/sour cream', 'yogurt', 'UHT-milk', 'condensed milk'],
    'Meat': ['beef', 'chicken', 'frankfurter', 'ham', 'pork', 'sausage', 'turkey'],
    'Produce': ['berries', 'citrus fruit', 'fruit/vegetable juice', 'grapes', 'onions', 'other vegetables', 'pip fruit', 'root vegetables', 'tropical fruit', 'packaged fruit/vegetables'],
    'Bakery': ['bread', 'brown bread', 'pastry', 'rolls/buns', 'white bread', 'zwieback', 'long life bakery product', 'cake bar'],
    'Beverages': ['beverages', 'bottled beer', 'bottled water', 'canned beer', 'coffee', 'misc. beverages', 'soda', 'tea', 'brandy', 'liquor', 'wine'],
    'Pantry': ['cereals', 'chocolate', 'candy', 'flour', 'margarine', 'oil', 'rice', 'salt', 'sugar', 'sweet spreads', 'vinegar', 'abrasive cleaner', 'artif. sweetener', 'baking powder', 'bathroom cleaner', 'candles', 'cleaner', 'detergent', 'dish cleaner', 'dishes', 'frozen dessert', 'frozen vegetables', 'hard cheese', 'honey', 'house keeping products', 'hygiene articles', 'instant food products', 'jam', 'ketchup', 'light bulbs', 'liqueur', 'mayonnaise', 'mustard', 'napkins', 'newspapers', 'nut snack', 'nuts/prunes', 'pasta', 'pet care', 'photo/film', 'pickled vegetables', 'popcorn', 'pudding powder', 'ready soups', 'salty snack', 'semi-finished bread', 'shopping bags', 'skin care', 'soap', 'soft cheese', 'softener', 'soups', 'spices', 'specialty bar', 'specialty cheese', 'specialty chocolate', 'specialty fat', 'spread cheese', 'sugar', 'sweet spreads', 'syrup', 'tidbits', 'turkey', 'waffles', 'whisky', 'white wine', 'zwieback']
}

# Assign categories
categorized_items = []
for item in new_items:
    item_lower = item.lower()
    assigned_cat = 'Pantry'  # default
    for cat, keywords in categories.items():
        if any(keyword in item_lower for keyword in keywords):
            assigned_cat = cat
            break
    categorized_items.append((item, assigned_cat))

# Price ranges
price_ranges = {
    'Dairy': (2.5, 8.0),
    'Meat': (5.0, 15.0),
    'Produce': (1.0, 6.0),
    'Bakery': (2.0, 7.0),
    'Beverages': (1.5, 12.0),
    'Pantry': (1.0, 10.0)
}

random.seed(42)  # for reproducibility

# Create new products
next_id = max(p['id'] for p in existing_products) + 1
new_products = []
for item, cat in categorized_items:
    min_price, max_price = price_ranges[cat]
    price = round(random.uniform(min_price, max_price), 2)
    new_products.append({
        'id': next_id,
        'name': item,
        'price': price,
        'category': cat
    })
    next_id += 1

# Write back to CSV
all_products = existing_products + new_products
with open('ml_models/products.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'price', 'category'])
    writer.writeheader()
    for product in all_products:
        writer.writerow(product)

print(f'Total products now: {len(all_products)}')
print('Sample new products:')
for p in new_products[:10]:
    print(f'{p["id"]}: {p["name"]} - ${p["price"]} ({p["category"]})')4
    
    