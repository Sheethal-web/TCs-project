from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="Raspberry Pi Edge AI Server")

# Load the pre-trained massive rules locally on the Pi
# We do NOT train on the Pi. We only do inference to keep it lightning fast.
rules_path = os.path.join(os.path.dirname(__file__), 'massive_trained_rules.csv')

try:
    print("Loading Pre-Trained AI Rules into Raspberry Pi Memory...")
    rules_df = pd.read_csv(rules_path)
    # Convert string representation back to lists for easy searching
    rules_df['antecedents'] = rules_df['antecedents'].apply(lambda x: [i.strip() for i in x.split(',')])
    print(f"✅ Loaded {len(rules_df)} ML rules successfully for Offline Inference!")
except FileNotFoundError:
    print("Warning: Rules file not found. Please sync from AWS or run the training script.")
    rules_df = pd.DataFrame()

class CartRequest(BaseModel):
    items: list[str]

@app.get("/")
def health_check():
    return {"status": "Raspberry Pi Edge AI Online", "rules_loaded": len(rules_df)}

@app.post("/api/ai/bundle")
def get_edge_bundle(req: CartRequest):
    """
    Lightning fast offline inference. 
    Checks the local CSV rules to push a coupon to the POS Kiosk.
    """
    if rules_df.empty:
        return {"recommendation": None}

    cart_items = set(req.items)
    
    # Scan rules to see if cart matches any triggers
    for _, row in rules_df.iterrows():
        trigger_items = set(row['antecedents'])
        if trigger_items.issubset(cart_items):
            # Check if the consequent (recommendation) is NOT already in the cart
            consequent = row['consequents'].strip()
            if consequent not in cart_items:
                return {
                    "trigger": list(trigger_items),
                    "recommendation": consequent,
                    "confidence": round(row['confidence'] * 100, 2),
                    "lift": round(row['lift'], 2),
                    "message": f"Edge AI: High confidence ({round(row['confidence']*100)}%) bundle found!"
                }
    
    return {"recommendation": None}

# To run on the Raspberry Pi:
# pip install fastapi uvicorn pandas
# uvicorn rpi_edge_server:app --host 0.0.0.0 --port 8000
