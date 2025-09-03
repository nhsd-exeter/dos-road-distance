import json
import os
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


class FiveDest(HttpUser):
    weight = 1
    host = config.BASE_HOST
    wait_time = between(1, 3)  # Add wait time between requests
    
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

    @tag('load')
    @task
    def do_test(self):
        if current_file.get_file() != self.current_payload_file:
            self.load_payload()
        self.client.post(config.API_ENDPOINT, data=self.payload, headers=config.headers)


class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 600, "users": 20, "spawn_rate": 2, "request_file": "ccs_50_destinations.json"},
        {"duration": 1200, "users": 40, "spawn_rate": 3, "request_file": "ccs_50_destinations.json"},
        {"duration": 1800, "users": 60, "spawn_rate": 4, "request_file": "ccs_50_destinations.json"},
        {"duration": 2400, "users": 80, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},
        {"duration": 3000, "users": 100, "spawn_rate": 6, "request_file": "ccs_50_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
