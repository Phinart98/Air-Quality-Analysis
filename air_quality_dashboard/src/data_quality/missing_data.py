class MissingDataHandler:
    def __init__(self, data):
        self.data = data
    
    def interpolate_missing(self, method='linear'):
        return self.data.interpolate(method=method)
    
    def forward_fill(self, limit=None):
        return self.data.ffill(limit=limit)
    
    def backward_fill(self, limit=None):
        return self.data.bfill(limit=limit)
    
    def fill_with_mean(self):
        return self.data.fillna(self.data.mean())
    
    def get_missing_patterns(self):
        missing_patterns = {}
        for column in self.data.columns:
            missing_count = self.data[column].isnull().sum()
            missing_percentage = (missing_count / len(self.data)) * 100
            missing_patterns[column] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
        return missing_patterns
