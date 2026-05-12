import pandas as pd
import numpy as np
import random
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os
import sys

def train_on_internet_data():
    print("\n--- DOWNLOADING DATA FROM INTERNET ---")
    print("Fetching the 'Online Retail' / 'Groceries' public dataset from Kaggle/UCI...")
    # Using a common public Market Basket CSV (Groceries dataset)
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/groceries.csv"
    
    try:
        # The CSV has variable number of columns per row.
        with open('temp_groceries.csv', 'wb') as f:
            import urllib.request
            f.write(urllib.request.urlopen(url).read())
            
        with open('temp_groceries.csv', 'r') as f:
            transactions = [line.strip().split(',') for line in f.readlines()]
            
        print(f"Successfully downloaded {len(transactions)} real-world transactions!")
        
        print("Preprocessing Data...")
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        print("Training FP-Growth on Internet Data...")
        frequent_itemsets = fpgrowth(df, min_support=0.01, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
        rules = rules.sort_values(by='lift', ascending=False)
        
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        output_path = os.path.join(os.path.dirname(__file__), 'internet_trained_rules.csv')
        rules.to_csv(output_path, index=False)
        print(f"Saved Internet Rules to: {output_path}")
        print(rules[['antecedents', 'consequents', 'lift']].head(5))
        
    except Exception as e:
        print(f"Error downloading or training on internet data: {e}")


def train_on_custom_categories():
    print("--- 1. Generating Custom Category Data (20,000 Transactions) ---")
    # Define our base products
    PRODUCTS = [
        'Laptop', 'Wireless Mouse', 'DSLR Camera', 'SD Card', 
        'Pasta', 'Garlic Bread', 'Burger', 'Large Fries',
        'Diapers', 'Wet Wipes', 'Notebooks (Set of 5)', 'Blue Pens',
        'Smart TV', 'Soundbar', 'Coffee', 'Almond Croissant',
        'Baby Lotion', 'Baby Wash', 'Backpack', 'Lunch Box'
    ]

    # Define underlying consumer patterns to inject into the dataset
    PATTERNS = [
        (['Laptop'], ['Wireless Mouse'], 0.65), 
        (['DSLR Camera'], ['SD Card'], 0.70),
        (['Pasta'], ['Garlic Bread'], 0.80),
        (['Burger'], ['Large Fries'], 0.85),
        (['Diapers'], ['Wet Wipes'], 0.90),
        (['Notebooks (Set of 5)'], ['Blue Pens'], 0.50),
        (['Smart TV'], ['Soundbar'], 0.40),
        (['Coffee'], ['Almond Croissant'], 0.60),
        (['Baby Lotion'], ['Baby Wash'], 0.75),
        (['Backpack'], ['Lunch Box'], 0.55),
    ]

    transactions = []
    num_transactions = 20000

    for _ in range(num_transactions):
        cart = []
        num_random_items = random.randint(1, 3)
        cart.extend(random.sample(PRODUCTS, num_random_items))
        
        for trigger, consequent, prob in PATTERNS:
            if all(item in cart for item in trigger):
                if random.random() < prob:
                    cart.extend(consequent)
                    
        cart = list(set(cart))
        transactions.append(cart)

    print("--- 2. Preprocessing Custom Data ---")
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    print(f"Data Shape: {df.shape}. Training Model via FP-Growth...")
    frequent_itemsets = fpgrowth(df, min_support=0.01, use_colnames=True)

    print("--- 3. Extracting Association Rules ---")
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
    rules = rules.sort_values(by='lift', ascending=False)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

    output_path = os.path.join(os.path.dirname(__file__), 'trained_rules.csv')
    rules.to_csv(output_path, index=False)

    print(f"--- 4. Custom Model Trained! Saved {len(rules)} rules to: {output_path} ---")
    print(rules[['antecedents', 'consequents', 'lift']].head(5))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--internet':
        train_on_internet_data()
    else:
        train_on_custom_categories()
        print("\nTip: Run 'python train_model.py --internet' to train on a real public dataset from the internet instead!")

