import numpy as np
from scipy import stats

class OutlierDetector:
    def __init__(self, data):
        self.data = data
    
    def detect_zscore_outliers(self, threshold=3):
        outliers = {}
        for column in self.data.select_dtypes(include=[np.number]).columns:
            z_scores = np.abs(stats.zscore(self.data[column].dropna()))
            outliers[column] = np.where(z_scores > threshold)[0]
        return outliers
    
    def detect_iqr_outliers(self):
        outliers = {}
        for column in self.data.select_dtypes(include=[np.number]).columns:
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers[column] = self.data[
                (self.data[column] < (Q1 - 1.5 * IQR)) | 
                (self.data[column] > (Q3 + 1.5 * IQR))
            ].index
        return outliers
    
    def remove_outliers(self, method='zscore', threshold=3):
        if method == 'zscore':
            outliers = self.detect_zscore_outliers(threshold)
        else:
            outliers = self.detect_iqr_outliers()
        
        clean_data = self.data.copy()
        for column, indices in outliers.items():
            clean_data.loc[indices, column] = np.nan
        return clean_data
