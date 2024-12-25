import seaborn as sns
import matplotlib.pyplot as plt

class CorrelationMatrix:
    def __init__(self, data):
        self.data = data
        
    def create_correlation_matrix(self):
        numeric_cols = ['pm10', 'pm25']
        valid_data = self.data[numeric_cols].dropna()
        
        if valid_data.empty:
            return None
            
        corr = valid_data.corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Pollutant Correlation Matrix')
        return plt.gcf()
