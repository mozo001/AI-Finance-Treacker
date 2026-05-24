# tracker/predictor.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import Transaction

def predict_next_month_expense(user):
    # Fetch historical daily expense aggregates for this user
    queryset = Transaction.objects.filter(user=user, transaction_type='expense')
    
    # We need at least some data points to draw a prediction line
    if queryset.count() < 3: 
        return "Not enough data history to predict yet."
        
    # Convert Django queryset to a Pandas DataFrame
    df = pd.DataFrame(list(queryset.values('date', 'amount')))
    
    # Group by date to handle multiple expenses in a single day
    df_daily = df.groupby('date')['amount'].sum().reset_index()
    
    # Convert dates to numerical ordinals so scikit-learn can read them
    df_daily['date_ordinal'] = df_daily['date'].apply(lambda x: x.toordinal())
    
    X = df_daily[['date_ordinal']].values
    y = df_daily['amount'].values
    
    # Train a quick Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for 30 days into the future from the last recorded date
    last_date_ordinal = X[-1][0]
    future_date = np.array([[last_date_ordinal + 30]])
    prediction = model.predict(future_date)
    
    # Return the predicted amount rounded cleanly, ensuring it's not negative
    return f"${max(0, round(float(prediction[0]), 2))}"