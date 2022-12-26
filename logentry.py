import json


class LogEntry:

    def __init__(self, timestamp, url, status_code, pattern_found, response_time):
        self.timestamp = timestamp
        self.url = url
        self.status_code = status_code
        self.pattern_found = pattern_found
        self.response_time = response_time

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return f"{self.timestamp}; target={self.url}; status_code={self.status_code}; pattern_found={self.pattern_found}; response_time_seconds={self.response_time:.2f}"
