import json
import os
from locust import HttpUser, task, LoadTestShape, tag, between
import config as config

# Debug: Print all relevant environment variables and configuration
print("=== SCENARIO2 DEBUG CONFIGURATION ===")
print(f"config.BASE_HOST = {config.BASE_HOST}")
print(f"config.API_ENDPOINT = {config.API_ENDPOINT}")
print(f"Environment PERF_TEST_HOST = {os.environ.get('PERF_TEST_HOST', 'NOT SET')}")
print(f"Environment LOCUST_HOST = {os.environ.get('LOCUST_HOST', 'NOT SET')}")
print("=== END SCENARIO2 DEBUG ===")


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
    wait_time = between(0.5, 2)
    host = config.BASE_HOST  # Add missing host configuration

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: scenario2 User host = {self.host}")
        # Load initial payload
        self.load_payload()

    def load_payload(self):
        """Load payload based on current file setting"""
        with open(f'{config.ccs_prefix}{current_file.get_file()}') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def do_test(self):
        # Reload payload in case file has changed
        self.load_payload()
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 600, "users": 30, "spawn_rate": 10, "request_file": "ccs_50_destinations.json"},
        {"duration": 1200, "users": 60, "spawn_rate": 20, "request_file": "ccs_50_destinations.json"},
        {"duration": 1800, "users": 90, "spawn_rate": 30, "request_file": "ccs_50_destinations.json"},
        {"duration": 2400, "users": 120, "spawn_rate": 40, "request_file": "ccs_50_destinations.json"},
        {"duration": 3000, "users": 150, "spawn_rate": 50, "request_file": "ccs_50_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
