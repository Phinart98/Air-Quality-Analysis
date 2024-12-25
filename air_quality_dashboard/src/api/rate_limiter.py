import time
from collections import deque
from datetime import datetime

class RateLimiter:
    def __init__(self, max_requests=60, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def can_make_request(self):
        now = datetime.now()
        while self.requests and (now - self.requests[0]).seconds > self.time_window:
            self.requests.popleft()
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def wait_for_next_window(self):
        while not self.can_make_request():
            time.sleep(1)
