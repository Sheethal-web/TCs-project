import pandas as pd
import numpy as np

# Note: In a real-world scenario, you would install the following libraries:
# pip install mlxtend scikit-learn
# from mlxtend.frequent_patterns import apriori, association_rules
# from sklearn.ensemble import RandomForestRegressor

class MarketBasketAnalyzer:
    """
    1. Market Basket Analysis (The "Bundler")
    Answers: "What else will this customer buy?"
    Algorithm: Apriori or FP-Growth.
    """
    def __init__(self):
        # Mock Association Rules generated from past receipts
        self.rules = pd.DataFrame({
            'antecedents': [frozenset({'Mutton Curry'}), frozenset({'Steak'})],
            'consequents': [frozenset({'Cold Coffee'}), frozenset({'Red Wine'})],
            'support': [0.15, 0.12],
            'confidence': [0.65, 0.70],
            'lift': [2.4, 3.1] # Lift > 1 means they are likely to be bought together
        })

    def get_bundle_recommendation(self, current_cart_items):
        """
        If a user adds 'Mutton Curry', check rules. If lift > 2.0, recommend 'Cold Coffee'.
        """
        for item in current_cart_items:
            # Find rules where the antecedent matches the cart item
            match = self.rules[self.rules['antecedents'] == frozenset({item})]
            if not match.empty:
                best_rule = match.sort_values(by='lift', ascending=False).iloc[0]
                if best_rule['lift'] > 2.0:
                    recommended_item = list(best_rule['consequents'])[0]
                    return {
                        'trigger': item,
                        'recommendation': recommended_item,
                        'reason': f"Lift: {best_rule['lift']} - Highly bought together"
                    }
        return None


class SalesPredictor:
    """
    2. Time-Series Forecasting (The "Predictor")
    Answers: "How much will I sell by the end of the day?"
    Algorithm: Random Forest Regressor or Prophet.
    """
    def __init__(self):
        # In a real model: self.model = RandomForestRegressor().fit(X_train, y_train)
        pass

    def predict_end_of_day_sales(self, item_name, current_time, weather, day_of_week):
        """
        Mock prediction logic based on time-series patterns.
        """
        # The AI notices that on rainy Tuesdays, Soup sells 50% more.
        if item_name == 'Tomato Soup' and weather == 'Rainy' and day_of_week == 'Tuesday':
            return {"predicted_sales": 45, "status": "High Demand"}
            
        # Default mock prediction
        if item_name == 'Fresh Juice' and weather == 'Rainy':
            return {"predicted_sales": 5, "status": "Waste Risk"} # Drop in sales
            
        return {"predicted_sales": 20, "status": "Normal"}


class PricingOptimizer:
    """
    3. Reinforcement Learning (The "Optimizer")
    Answers: "What is the smallest discount I can give to make them buy?"
    Algorithm: Q-Learning or Markov Decision Process (MDP).
    """
    def __init__(self):
        # Simple Mock Q-Table
        # States: [Inventory High, Sales Low]
        # Actions (Discounts): [5%, 10%, 15%, 20%, 50%]
        # Values: Q-Values (Expected Reward/Profit)
        self.q_table = {
            'High_Inv_Low_Sales': {
                '5%': 10,
                '10%': 25,
                '15%': 80,  # 15% is the sweet spot
                '20%': 70,  # Loses too much margin
                '50%': 20   # Terrible margin, even if it sells
            }
        }

    def get_optimal_discount(self, inventory_level, current_sales_velocity):
        state = f"{inventory_level}_Inv_{current_sales_velocity}_Sales"
        
        if state in self.q_table:
            actions = self.q_table[state]
            # Choose the action with the highest Q-Value (Exploitation)
            best_discount = max(actions, key=actions.get)
            return best_discount
        return "10%" # Default safe fallback


# --- Example Execution (Simulating the Backend checking for a user) ---
if __name__ == "__main__":
    print("--- 1. MARKET BASKET ANALYSIS (The Bundler) ---")
    bundler = MarketBasketAnalyzer()
    cart = ['Mutton Curry']
    rec = bundler.get_bundle_recommendation(cart)
    if rec:
        print(f"Customer added {rec['trigger']}. AI Recommends {rec['recommendation']} ({rec['reason']})")
        
    print("\n--- 2. TIME-SERIES FORECASTING (The Predictor) ---")
    predictor = SalesPredictor()
    juice_pred = predictor.predict_end_of_day_sales("Fresh Juice", "14:00", "Rainy", "Tuesday")
    print(f"Fresh Juice Prediction (Rainy Tuesday): {juice_pred['predicted_sales']} units. Risk: {juice_pred['status']}")
    
    print("\n--- 3. REINFORCEMENT LEARNING (The Optimizer) ---")
    optimizer = PricingOptimizer()
    if juice_pred['status'] == "Waste Risk":
        # We need to discount it to avoid waste
        best_discount = optimizer.get_optimal_discount("High", "Low")
        print(f"AI suggests markdown for Fresh Juice. Optimal Discount to maximize profit: {best_discount}")

