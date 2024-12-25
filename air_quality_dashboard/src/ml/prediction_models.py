from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class PollutionPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.feature_columns = None
        
    def prepare_features(self, data):
        features = data.copy()
        features['hour'] = features.index.hour
        features['day'] = features.index.day
        features['month'] = features.index.month
        features['day_of_week'] = features.index.dayofweek
        return features
        
    def train(self, data, target_column='pm10'):
        features = self.prepare_features(data)
        self.feature_columns = [col for col in features.columns 
                              if col != target_column]
        
        X = features[self.feature_columns]
        y = features[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        return self.model.score(X_test, y_test)
        
    def predict(self, data):
        features = self.prepare_features(data)
        return self.model.predict(features[self.feature_columns])
