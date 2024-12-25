class DataValidator:
    def __init__(self, data):
        self.data = data
        self.validation_rules = {
            'pm10': {'min': 0, 'max': 1000},
            'pm25': {'min': 0, 'max': 500},
            'no2': {'min': 0, 'max': 2000},
            'o3': {'min': 0, 'max': 500}
        }
    
    def check_value_ranges(self):
        validation_results = {}
        for column, rules in self.validation_rules.items():
            if column in self.data.columns:
                out_of_range = self.data[
                    (self.data[column] < rules['min']) | 
                    (self.data[column] > rules['max'])
                ]
                validation_results[column] = len(out_of_range)
        return validation_results
    
    def check_missing_values(self):
        return self.data.isnull().sum()
    
    def check_data_types(self):
        return self.data.dtypes.to_dict()
