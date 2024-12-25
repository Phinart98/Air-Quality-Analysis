import logging
from functools import wraps
import requests

class APIErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def handle_request_error(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                self.logger.error(f"API Request failed: {str(e)}")
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                raise
        return wrapper
