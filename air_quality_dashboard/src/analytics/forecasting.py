from prophet import Prophet
import pandas as pd

class TimeSeriesForecaster:
    def __init__(self):
        self.model = Prophet()
        
    def forecast(self, data, periods=30):
        df = pd.DataFrame({
            'ds': data.index,
            'y': data.values
        })
        
        self.model.fit(df)
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
