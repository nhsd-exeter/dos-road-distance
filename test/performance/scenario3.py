import json
from locust import HttpUser, task, LoadTestShape, tag, between
import config as config

class LoadFile:
    def __init__(self):
        self.file = "ccs_5_destinations.json"

    def set_file(self, file: str):
        self.file = file

    def get_file(self):
        return self.file


current_file = LoadFile()


class StepDownStressUser(HttpUser):
    host = config.BASE_HOST
    wait_time = between(0.1, 0.3)

    def on_start(self):
        self.payload_cache = {}
        self.current_payload_file = None
        self.load_payload()

    def load_payload(self):
        """Load and cache payload based on current file setting"""
        file_name = current_file.get_file()
        if file_name != self.current_payload_file or file_name not in self.payload_cache:
            with open(f'{config.ccs_prefix}{file_name}') as json_file:
                self.payload_cache[file_name] = json.dumps(json.load(json_file))
            self.current_payload_file = file_name
        self.payload = self.payload_cache[file_name]

    @tag('step_down')
    @task
    def stress_request(self):
        if current_file.get_file() != self.current_payload_file:
            self.load_payload()
        
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


class StepDownLoadShape(LoadTestShape):
    stages = [
        {"duration": 600, "users": 150, "spawn_rate": 50, "request_file": "ccs_50_destinations.json"},
        {"duration": 1200, "users": 120, "spawn_rate": 40, "request_file": "ccs_50_destinations.json"},
        {"duration": 1800, "users": 90, "spawn_rate": 30, "request_file": "ccs_50_destinations.json"},
        {"duration": 2400, "users": 60, "spawn_rate": 20, "request_file": "ccs_50_destinations.json"},
        {"duration": 3000, "users": 30, "spawn_rate": 10, "request_file": "ccs_50_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
