class DataCleaningPipeline:
    def __init__(self, validator, missing_handler, outlier_detector):
        self.validator = validator
        self.missing_handler = missing_handler
        self.outlier_detector = outlier_detector
    
    def run_pipeline(self, data):
        # Step 1: Validate data
        validation_results = self.validator.check_value_ranges()
        missing_values = self.validator.check_missing_values()
        
        # Step 2: Handle missing values
        data = self.missing_handler.interpolate_missing()
        
        # Step 3: Remove outliers
        data = self.outlier_detector.remove_outliers()
        
        # Step 4: Final validation
        final_validation = self.validator.check_value_ranges()
        
        pipeline_results = {
            'initial_validation': validation_results,
            'missing_values_found': missing_values,
            'final_validation': final_validation,
            'cleaned_data': data
        }
        
        return pipeline_results
