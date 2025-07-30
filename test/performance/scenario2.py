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
        {"duration": 180, "users": 10, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},    # 0-3 min: 10 users
        {"duration": 360, "users": 20, "spawn_rate": 10, "request_file": "ccs_50_destinations.json"},   # 3-6 min: 20 users
        {"duration": 540, "users": 30, "spawn_rate": 15, "request_file": "ccs_50_destinations.json"},   # 6-9 min: 30 users
        {"duration": 720, "users": 40, "spawn_rate": 20, "request_file": "ccs_50_destinations.json"},   # 9-12 min: 40 users
        {"duration": 900, "users": 50, "spawn_rate": 25, "request_file": "ccs_50_destinations.json"},   # 12-15 min: 50 users
        {"duration": 1080, "users": 60, "spawn_rate": 30, "request_file": "ccs_50_destinations.json"},  # 15-18 min: 60 users
        {"duration": 1260, "users": 70, "spawn_rate": 35, "request_file": "ccs_50_destinations.json"},  # 18-21 min: 70 users
        {"duration": 1440, "users": 80, "spawn_rate": 40, "request_file": "ccs_50_destinations.json"},  # 21-24 min: 80 users
        {"duration": 1620, "users": 90, "spawn_rate": 45, "request_file": "ccs_50_destinations.json"},  # 24-27 min: 90 users
        {"duration": 1800, "users": 100, "spawn_rate": 50, "request_file": "ccs_50_destinations.json"}, # 27-30 min: 100 users
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
