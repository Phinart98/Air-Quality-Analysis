from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FeatureImportanceAnalyzer:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        
    def analyze_importance(self, X, y):
        self.model.fit(X, y)
        importance = self.model.feature_importances_
        
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': importance
        })
        return feature_importance.sort_values('importance', ascending=False)
        
    def plot_importance(self, feature_importance, top_n=10):
        plt.figure(figsize=(10, 6))
        plt.barh(
            feature_importance['feature'][:top_n],
            feature_importance['importance'][:top_n]
        )
        plt.title('Feature Importance Analysis')
        plt.xlabel('Importance Score')
        return plt
