import json
from locust import HttpUser, task, LoadTestShape, tag
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

    def on_start(self):
        with open(f'{config.ccs_prefix}{current_file.get_file()}') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def do_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 600, "users": 30, "spawn_rate": 10, "request_file": "ccs_3000_destinations.json"},
        {"duration": 1200, "users": 60, "spawn_rate": 20, "request_file": "ccs_3000_destinations.json"},
        {"duration": 1800, "users": 90, "spawn_rate": 30, "request_file": "ccs_3000_destinations.json"},
        {"duration": 2400, "users": 120, "spawn_rate": 40, "request_file": "ccs_3000_destinations.json"},
        {"duration": 3000, "users": 150, "spawn_rate": 50, "request_file": "ccs_3000_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
