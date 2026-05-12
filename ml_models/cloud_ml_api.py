from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="Cloud ML Bundle Predictor API")

# Load the rules that were trained by the massive data generator
rules_path = os.path.join(os.path.dirname(__file__), 'massive_trained_rules.csv')

try:
    print("Loading 1-Million Row Trained ML Rules into Cloud Memory...")
    rules_df = pd.read_csv(rules_path)
    # Convert 'antecedents' string into a list of strings
    rules_df['antecedents'] = rules_df['antecedents'].apply(lambda x: [i.strip() for i in str(x).split(',')])
    print(f"✅ Cloud ML Engine Ready. Loaded {len(rules_df)} intelligent rules.")
except FileNotFoundError:
    print("WARNING: massive_trained_rules.csv not found! Please run train_on_massive.py first.")
    rules_df = pd.DataFrame()

class CartRequest(BaseModel):
    items: list[str]

@app.post("/predict_bundle")
def get_prediction(req: CartRequest):
    """
    Receives a list of cart items and uses Market Basket Analysis
    to predict the best high-conversion item to bundle.
    """
    if rules_df.empty:
        return {"recommendation": None, "message": "ML Engine Offline"}

    cart_items = set(req.items)
    
    # Sort rules by highest Lift/Confidence (already done in training, but we iterate in order)
    for _, row in rules_df.iterrows():
        trigger_items = set(row['antecedents'])
        
        # If the customer's cart contains the trigger items (e.g., they have a Laptop)
        if trigger_items.issubset(cart_items):
            consequent = str(row['consequents']).strip()
            
            # If they haven't already bought the recommended item (e.g., Mouse)
            if consequent not in cart_items:
                discount_percentage = int(min(50, row['lift'] * 10)) # Dynamic discount based on lift
                return {
                    "recommendation": consequent,
                    "confidence": round(row['confidence'] * 100, 2),
                    "lift": round(row['lift'], 2),
                    "discountText": f"{discount_percentage}% OFF {consequent}",
                    "message": f"Cloud AI Prediction: Customers who buy {', '.join(trigger_items)} have a {round(row['confidence']*100)}% probability of buying {consequent}!"
                }
                
    return {"recommendation": None, "message": "No high-probability bundle found."}

if __name__ == "__main__":
    import uvicorn
    # Runs the Cloud ML Engine on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
