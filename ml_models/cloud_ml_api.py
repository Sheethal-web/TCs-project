from fastapi import FastAPI
from pydantic import BaseModel
import csv
import os

app = FastAPI(title="Cloud ML Bundle Predictor API")

# Load the rules that were trained by the massive data generator
rules_path = os.path.join(os.path.dirname(__file__), 'massive_trained_rules.csv')

def parse_items(value):
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]
    return []


def load_rules(path):
    rules = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            antecedents = set(parse_items(row.get('antecedents', '')))
            consequents = [item for item in parse_items(row.get('consequents', '')) if item]
            lift = float(row.get('lift', 0) or 0)
            confidence = float(row.get('confidence', 0) or 0)
            if antecedents and consequents:
                rules.append({
                    'antecedents': antecedents,
                    'consequents': consequents,
                    'support': float(row.get('support', 0) or 0),
                    'confidence': confidence,
                    'lift': lift
                })
    return rules

try:
    print("Loading 1-Million Row Trained ML Rules into Cloud Memory...")
    rules_df = load_rules(rules_path)
    print(f"✅ Cloud ML Engine Ready. Loaded {len(rules_df)} intelligent rules.")
except FileNotFoundError:
    print("WARNING: massive_trained_rules.csv not found! Please run train_on_massive.py first.")
    rules_df = []

class CartRequest(BaseModel):
    items: list[str]

@app.post("/predict_bundle")
def get_prediction(req: CartRequest):
    """
    Receives a list of cart items and uses Market Basket Analysis
    to predict the best high-conversion item to bundle.
    """
    if not rules_df:
        return {"recommendation": None, "message": "ML Engine Offline"}

    cart_items = set(req.items)
    
    # Sort rules by highest Lift/Confidence (already done in training, but we iterate in order)
    for row in rules_df:
        trigger_items = row['antecedents']
        
        if trigger_items.issubset(cart_items):
            for consequent in row['consequents']:
                if consequent and consequent not in cart_items:
                    discount_percentage = int(min(50, row['lift'] * 10)) # Dynamic discount based on lift
                    return {
                        "recommendation": consequent,
                        "confidence": round(row['confidence'] * 100, 2),
                        "lift": round(row['lift'], 2),
                        "discountText": f"{discount_percentage}% OFF {consequent}",
                        "message": f"Cloud AI Prediction: Customers who buy {', '.join(trigger_items)} have a {round(row['confidence']*100)}% probability of buying {consequent}!"
                    }

    # Fallback recommendations for demo products not present in the training file
    fallback_rules = [
        {'antecedents': {'Smartphone'}, 'consequent': 'Wireless Earbuds', 'lift': 2.8, 'confidence': 0.72},
        {'antecedents': {'Laptop'}, 'consequent': 'Laptop Bag', 'lift': 2.6, 'confidence': 0.68},
        {'antecedents': {'Tablet'}, 'consequent': 'Tablet Case', 'lift': 2.4, 'confidence': 0.65}
    ]

    for fallback in fallback_rules:
        if fallback['antecedents'].issubset(cart_items) and fallback['consequent'] not in cart_items:
            discount_percentage = int(min(50, fallback['lift'] * 10))
            return {
                "recommendation": fallback['consequent'],
                "confidence": round(fallback['confidence'] * 100, 2),
                "lift": round(fallback['lift'], 2),
                "discountText": f"{discount_percentage}% OFF {fallback['consequent']}",
                "message": f"Demo Fallback: Customers who buy {', '.join(fallback['antecedents'])} often also buy {fallback['consequent']}."
            }

    return {"recommendation": None, "message": "No high-probability bundle found."}

if __name__ == "__main__":
    import uvicorn
    # Runs the Cloud ML Engine on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
