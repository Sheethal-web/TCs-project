#!/usr/bin/env python3
"""
Simulation script for product selection, recommendations, and coupon generation.
This script simulates a user interacting with the system:
1. Selecting products from 3 options
2. Getting ML-based recommendations
3. Adding to cart with discounted coupons
"""

import sys
import os
import csv
sys.path.append(os.path.dirname(__file__))

from coupon_ai import MarketBasketAnalyzer
import random

PRODUCTS_CSV = os.path.join(os.path.dirname(__file__), 'products.csv')


def load_products(csv_path):
    products = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'price': float(row['price']),
                    'category': row['category']
                })
    except FileNotFoundError:
        products = [
            {'id': 1, 'name': 'Smartphone', 'price': 209, 'category': 'Electronics'},
            {'id': 2, 'name': 'Laptop', 'price': 679, 'category': 'Electronics'},
            {'id': 3, 'name': 'Tablet', 'price': 979, 'category': 'Electronics'},
            {'id': 4, 'name': 'Wireless Earbuds', 'price': 99, 'category': 'Electronics'},
            {'id': 5, 'name': 'Laptop Bag', 'price': 49, 'category': 'Accessories'},
            {'id': 6, 'name': 'Tablet Case', 'price': 39, 'category': 'Accessories'},
        ]
    return products

PRODUCTS = load_products(PRODUCTS_CSV)

class CartSimulator:
    def __init__(self):
        self.cart = []
        self.analyzer = MarketBasketAnalyzer()

    def select_product(self):
        """Simulate user selecting a product by entering a valid ID from the catalog."""
        # Randomly select 12 products to show (to keep the interface manageable)
        import random
        available_products = random.sample(PRODUCTS, min(12, len(PRODUCTS)))

        print("Available products (random selection):")
        for prod in available_products:
            print(f"{prod['id']}. {prod['name']} - ${prod['price']}")

        valid_ids = [prod['id'] for prod in available_products]
        while True:
            try:
                choice = int(input(f"Select a product ({min(valid_ids)}-{max(valid_ids)}): "))
                if choice in valid_ids:
                    selected = next(prod for prod in PRODUCTS if prod['id'] == choice)
                    print(f"Selected: {selected['name']}")
                    return selected
                else:
                    print(f"Please enter one of the following IDs: {', '.join(str(i) for i in sorted(valid_ids))}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_recommendations(self, cart_items, show_message=True):
        """Get recommendations based on current cart"""
        item_names = []
        for item in cart_items:
            if isinstance(item, dict) and 'item' in item and isinstance(item['item'], dict):
                item_names.append(item['item']['name'])
            elif isinstance(item, dict) and 'name' in item:
                item_names.append(item['name'])
        rec = self.analyzer.get_bundle_recommendation(item_names)
        if not rec:
            if show_message:
                print("No recommendations available from the ML model for the current cart.")
            return []

        recommendation = rec['recommendation']
        if isinstance(recommendation, str):
            recommendation_list = [recommendation]
        else:
            recommendation_list = list(recommendation)

        if show_message:
            trigger_text = ", ".join(rec['trigger']) if isinstance(rec['trigger'], list) else str(rec['trigger'])
            print(f"ML Recommendation: Based on [{trigger_text}], we recommend {', '.join(recommendation_list)}")
            print(f"Reason: {rec['reason']}")
        return recommendation_list

    def generate_coupon(self, item):
        """Generate a discounted coupon for the item"""
        discount_percent = random.randint(5, 20)  # Random discount 5-20%
        original_price = item['price']
        discount_amount = original_price * discount_percent / 100
        discounted_price = original_price - discount_amount

        coupon = {
            'item': item['name'],
            'original_price': original_price,
            'discount_percent': discount_percent,
            'discounted_price': round(discounted_price, 2),
            'code': f"COUPON{random.randint(1000,9999)}"
        }

        print(f"Coupon generated: {discount_percent}% off {item['name']}!")
        print(f"Original: ${original_price}, Discounted: ${coupon['discounted_price']}")
        print(f"Coupon Code: {coupon['code']}")
        return coupon

    def add_to_cart(self, item):
        """Add item to cart with coupon"""
        coupon = self.generate_coupon(item)
        existing = next((c for c in self.cart if c['item']['id'] == item['id']), None)
        if existing:
            existing['qty'] += 1
            existing['coupon'] = coupon
            print(f"Updated quantity for {item['name']} to {existing['qty']} and refreshed coupon.\n")
        else:
            cart_item = {
                'item': item,
                'coupon': coupon,
                'qty': 1
            }
            self.cart.append(cart_item)
            print(f"Added {item['name']} to cart with coupon.\n")

    def show_cart(self):
        """Display current cart"""
        if not self.cart:
            print("Cart is empty.")
            return

        print("Current Cart:")
        total = 0
        for item in self.cart:
            discounted_price = item['coupon']['discounted_price']
            print(f"- {item['item']['name']}: ${discounted_price} (was ${item['item']['price']}) - Code: {item['coupon']['code']}")
            total += discounted_price
        print(f"Total: ${round(total, 2)}\n")

    def finalize_recommendation(self):
        """Provide a final ML recommendation when the user is done shopping."""
        if not self.cart:
            print("No cart items available for final recommendation.")
            return

        print("\nFinal recommendation check based on your selected products:")
        final_recs = self.get_recommendations(self.cart)
        if final_recs:
            print(f"Final ML suggested next item(s): {', '.join(final_recs)}")
        else:
            print("The ML model did not find an additional bundle recommendation for your final cart.")

def main():
    simulator = CartSimulator()

    print("Welcome to the Product Selection Simulator!")
    print("=" * 50)

    while True:
        selected = simulator.select_product()

        add_selected = input(f"Add {selected['name']} to cart with a coupon? (y/n): ").strip().lower()
        if add_selected == 'y':
            simulator.add_to_cart(selected)
        else:
            print(f"Skipped adding {selected['name']} to cart.")

        recommendations = simulator.get_recommendations(simulator.cart)

        if recommendations:
            add_rec = input("Add recommended items to cart? (y/n): ").strip().lower()
            if add_rec == 'y':
                for rec_name in recommendations:
                    rec_product = next((p for p in PRODUCTS if p['name'] == rec_name), None)
                    if rec_product:
                        simulator.add_to_cart(rec_product)
                    else:
                        print(f"Recommended item {rec_name} is not in catalog, but is still returned by the ML model.")
            else:
                print("Skipped adding ML recommended items.")

        simulator.show_cart()

        cont = input("Add another product? (y/n): ").strip().lower()
        if cont != 'y':
            simulator.finalize_recommendation()
            break

    print("Simulation complete!")

if __name__ == "__main__":
    main()