import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os
import time

print("--- 1. LOADING MASSIVE DATASET ---")
file_path = os.path.join(os.path.dirname(__file__), 'massive_sales_data.csv')

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please wait for the generation script to finish.")
    exit(1)

start_time = time.time()

# We will load a subset if it's too large for local memory, but pandas can usually handle 2M rows.
# To ensure fast execution during the demo, we sample 100,000 transactions.
print("Reading CSV (Grouping by Transaction_ID)...")
df = pd.read_csv(file_path, usecols=['Transaction_ID', 'Product_Name'])

print(f"Loaded {len(df):,} individual items. Grouping into shopping carts...")
# Group by Transaction_ID and convert to list of items
transactions = df.groupby('Transaction_ID')['Product_Name'].apply(list).values.tolist()

print(f"Total Unique Shopping Carts: {len(transactions):,}")

print("\n--- 2. PREPROCESSING FOR MACHINE LEARNING ---")
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
basket_df = pd.DataFrame(te_ary, columns=te.columns_)

print("\n--- 3. TRAINING FP-GROWTH MODEL ON BIG DATA ---")
# Lower min_support because our items are spread across many categories
frequent_itemsets = fpgrowth(basket_df, min_support=0.01, use_colnames=True)

print("Extracting Association Rules...")
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)

# Sort by lift (highest confidence/correlation first)
rules = rules.sort_values(by='lift', ascending=False)

rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

output_path = os.path.join(os.path.dirname(__file__), 'massive_trained_rules.csv')
rules.to_csv(output_path, index=False)

end_time = time.time()

print(f"\n✅ TRAINING COMPLETE IN {end_time - start_time:.2f} SECONDS!")
print(f"Model discovered {len(rules)} powerful association rules from the massive dataset.")
print(f"Rules saved to: {output_path}")

print("\n🔥 TOP 5 AI DISCOVERED BUNDLES FROM MASSIVE DATA 🔥")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

