import json
import csv
import os
from typing import List, Dict, Any

def parse_items(value):
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]
    return []

def load_rules():
    """Load the trained rules from the CSV file"""
    rules = []
    # In Lambda, the file will be in the same directory or in a layer
    rules_path = os.path.join(os.path.dirname(__file__), 'massive_trained_rules.csv')

    try:
        with open(rules_path, newline='', encoding='utf-8') as f:
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
    except FileNotFoundError:
        print("WARNING: massive_trained_rules.csv not found!")
        return []

    return rules

# Load rules at cold start
RULES = load_rules()

def get_bundle_recommendation(cart_items: List[str]) -> Dict[str, Any]:
    """
    Get bundle recommendation based on cart items
    """
    if not RULES:
        return {"recommendation": None, "message": "ML Engine Offline"}

    cart_set = set(cart_items)

    # Sort rules by highest Lift/Confidence
    for row in RULES:
        trigger_items = row['antecedents']

        if trigger_items.issubset(cart_set):
            for consequent in row['consequents']:
                if consequent and consequent not in cart_set:
                    discount_percentage = int(min(50, row['lift'] * 10))
                    return {
                        "recommendation": consequent,
                        "confidence": round(row['confidence'] * 100, 2),
                        "lift": round(row['lift'], 2),
                        "discountText": f"{discount_percentage}% OFF {consequent}",
                        "message": f"Cloud AI Prediction: Customers who buy {', '.join(trigger_items)} have a {round(row['confidence']*100)}% probability of buying {consequent}!"
                    }

    # Fallback recommendations
    fallback_rules = [
        {'antecedents': {'Smartphone'}, 'consequent': 'Wireless Earbuds', 'lift': 2.8, 'confidence': 0.72},
        {'antecedents': {'Laptop'}, 'consequent': 'Laptop Bag', 'lift': 2.6, 'confidence': 0.68},
        {'antecedents': {'Tablet'}, 'consequent': 'Tablet Case', 'lift': 2.4, 'confidence': 0.65}
    ]

    for fallback in fallback_rules:
        if fallback['antecedents'].issubset(cart_set) and fallback['consequent'] not in cart_set:
            discount_percentage = int(min(50, fallback['lift'] * 10))
            return {
                "recommendation": fallback['consequent'],
                "confidence": round(fallback['confidence'] * 100, 2),
                "lift": round(fallback['lift'], 2),
                "discountText": f"{discount_percentage}% OFF {fallback['consequent']}",
                "message": f"Demo Fallback: Customers who buy {', '.join(fallback['antecedents'])} often also buy {fallback['consequent']}."
            }

    return {"recommendation": None, "message": "No high-probability bundle found."}

def lambda_handler(event, context):
    """
    AWS Lambda handler for recommendation prediction
    """
    try:
        # Parse the incoming request
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        cart_items = body.get('items', [])

        if not cart_items:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'No items provided in cart'
                })
            }

        # Get recommendation
        recommendation = get_bundle_recommendation(cart_items)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(recommendation)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }</content>
<parameter name="filePath">/workspaces/TCs-project/lambda_recommendation.py