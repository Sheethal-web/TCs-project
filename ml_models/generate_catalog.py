import json
import random
import os

categories = {
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Wireless Earbuds', 'Bluetooth Speaker', '4K TV', 'Soundbar', 'Gaming Console', 'VR Headset', 'Power Bank', 'HDMI Cable', 'USB-C Charger', 'Mechanical Keyboard', 'Gaming Mouse', 'Webcam', 'Microphone', 'External SSD', 'Flash Drive', 'Router'],
    'Groceries': ['Milk', 'Eggs', 'Bread', 'Butter', 'Cheese', 'Yogurt', 'Chicken Breast', 'Ground Beef', 'Salmon', 'Apples', 'Bananas', 'Oranges', 'Spinach', 'Tomatoes', 'Onions', 'Potatoes', 'Rice', 'Pasta', 'Tomato Sauce', 'Olive Oil'],
    'Snacks & Beverages': ['Potato Chips', 'Tortilla Chips', 'Salsa', 'Popcorn', 'Chocolate Bar', 'Gummy Bears', 'Cookies', 'Crackers', 'Cola', 'Diet Cola', 'Orange Juice', 'Apple Juice', 'Bottled Water', 'Sparkling Water', 'Energy Drink', 'Coffee Beans', 'Tea Bags', 'Beer (6-pack)', 'Red Wine', 'White Wine'],
    'Home & Kitchen': ['Blender', 'Coffee Maker', 'Toaster', 'Microwave', 'Air Fryer', 'Plates Set', 'Silverware Set', 'Wine Glasses', 'Mug', 'Frying Pan', 'Saucepan', 'Cutting Board', 'Knife Set', 'Tupperware', 'Dish Soap', 'Sponges', 'Paper Towels', 'Trash Bags', 'Broom', 'Mop'],
    'Personal Care': ['Shampoo', 'Conditioner', 'Body Wash', 'Bar Soap', 'Toothpaste', 'Toothbrush', 'Mouthwash', 'Deodorant', 'Shaving Cream', 'Razors', 'Lotion', 'Face Wash', 'Moisturizer', 'Sunscreen', 'Lip Balm', 'Cotton Swabs', 'Toilet Paper', 'Hand Sanitizer', 'Band-Aids', 'Pain Reliever'],
    'Clothing & Accessories': ['T-Shirt', 'Jeans', 'Shorts', 'Hoodie', 'Sweater', 'Jacket', 'Sneakers', 'Dress Shoes', 'Socks', 'Underwear', 'Hat', 'Beanie', 'Sunglasses', 'Belt', 'Watch', 'Backpack', 'Wallet', 'Umbrella', 'Scarf', 'Gloves'],
    'Office Supplies': ['Pens', 'Pencils', 'Highlighters', 'Markers', 'Notebook', 'Printer Paper', 'Sticky Notes', 'Paper Clips', 'Stapler', 'Staples', 'Tape', 'Scissors', 'Calculator', 'Folders', 'Binders', 'Whiteboard', 'Dry Erase Markers', 'Desk Lamp', 'Office Chair', 'Mousepad'],
    'Tools & Hardware': ['Hammer', 'Screwdriver Set', 'Wrench', 'Pliers', 'Tape Measure', 'Level', 'Utility Knife', 'Drill', 'Drill Bits', 'Screws', 'Nails', 'Duct Tape', 'WD-40', 'Paintbrush', 'Paint Roller', 'Extension Cord', 'Flashlight', 'Batteries (AA)', 'Batteries (AAA)', 'Work Gloves'],
    'Toys & Games': ['Lego Set', 'Action Figure', 'Doll', 'Board Game', 'Card Game', 'Puzzle', 'Stuffed Animal', 'Remote Control Car', 'Yo-Yo', 'Frisbee', 'Football', 'Basketball', 'Soccer Ball', 'Jump Rope', 'Chalk', 'Water Gun', 'Play-Doh', 'Crayons', 'Coloring Book', 'Kite'],
    'Pets': ['Dog Food', 'Cat Food', 'Dog Treats', 'Cat Treats', 'Dog Toy', 'Cat Toy', 'Leash', 'Collar', 'Dog Bed', 'Cat Bed', 'Litter Box', 'Cat Litter', 'Fish Food', 'Aquarium Filter', 'Bird Seed', 'Hamster Food', 'Pet Shampoo', 'Brush', 'Flea Collar', 'Waste Bags']
}

products = []
item_id = 1

# Base prices for realism
base_prices = {
    'Electronics': (20, 1000), 'Groceries': (2, 20), 'Snacks & Beverages': (1, 15),
    'Home & Kitchen': (10, 150), 'Personal Care': (3, 25), 'Clothing & Accessories': (10, 100),
    'Office Supplies': (2, 50), 'Tools & Hardware': (5, 100), 'Toys & Games': (5, 60), 'Pets': (5, 50)
}

for cat, items in categories.items():
    min_p, max_p = base_prices[cat]
    for name in items:
        price = random.randint(min_p, max_p)
        if price > 50:
            price = (price // 10) * 10 - 1 # Make it 99, 199, etc.
        elif price > 10:
            price = price - 0.01 # 19.99
        
        products.append({
            "id": item_id,
            "name": name,
            "price": round(price, 2),
            "category": cat
        })
        item_id += 1

js_content = f"export const MENU_ITEMS = {json.dumps(products, indent=2)};\n"

output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'data', 'products.js')
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w') as f:
    f.write(js_content)

print(f"Generated {len(products)} products and saved to {output_path}")

# Now we rewrite the generate_massive_data.py to use this JSON
