import json


class LogEntry:

    def __init__(self, timestamp, url, result, response_time):
        self.timestamp = timestamp
        self.url = url
        self.result = result
        self.response_time = response_time

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return f"{self.timestamp}; target={self.url}; result={self.result}; response_time_seconds={self.response_time:.2f}"
