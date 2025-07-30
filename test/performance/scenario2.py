import json
import os
import time
from locust import HttpUser, task, LoadTestShape, tag, events
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import config as config

# Debug: Print environment state after importing config
print("=== SCENARIO2.PY DEBUG START ===")
print(f"Environment PERF_TEST_HOST = '{os.environ.get('PERF_TEST_HOST', 'NOT SET')}'")
print(f"Environment LOCUST_HOST = '{os.environ.get('LOCUST_HOST', 'NOT SET')}'")
print(f"All environment variables containing 'HOST': {[(k, v) for k, v in os.environ.items() if 'HOST' in k.upper()]}")
print(f"Config imported successfully. BASE_HOST = '{config.BASE_HOST}'")
print("=== SCENARIO2.PY DEBUG END ===")


class LoadFile:
    def __init__(self):
        self.file = "ccs_5_destinations.json"
        self._cached_payload = None

    def set_file(self, file: str):
        if self.file != file:
            self.file = file
            self._cached_payload = None  # Clear cache when file changes

    def get_file(self):
        return self.file

    def get_cached_payload(self):
        return self._cached_payload

    def set_cached_payload(self, payload):
        self._cached_payload = payload


current_file = LoadFile()


class FiveDest(HttpUser):
    weight = 1
    host = config.BASE_HOST
    connection_timeout = 30.0  # Reduced from 60 for faster failures
    network_timeout = 30.0     # Reduced from 60 for faster failures

    def on_start(self):
        # Setup connection pooling for better performance
        retry_strategy = Retry(
            total=2,  # Reduced retries for faster feedback
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        self.client.mount("http://", adapter)
        self.client.mount("https://", adapter)

        self.load_payload()

    def load_payload(self):
        # Cache payload to avoid repeated file I/O
        if current_file.get_cached_payload() is None:
            try:
                with open(f'{config.ccs_prefix}{current_file.get_file()}') as json_file:
                    payload = json.load(json_file)
                    current_file.set_cached_payload(payload)
            except FileNotFoundError:
                print(f"Warning: File {current_file.get_file()} not found, using default")
                current_file.set_cached_payload({"default": "payload"})

        self.payload = current_file.get_cached_payload()

    @tag('load')
    @task
    def do_test(self):
        start_time = time.time()
        try:
            response = self.client.post(
                config.API_ENDPOINT,
                json=self.payload,  # Use json parameter instead of data+dumps for efficiency
                headers=config.headers,
                timeout=15,  # Reduced timeout for faster feedback
                catch_response=True
            )

            response_time = time.time() - start_time

            # More detailed response handling
            if response.status_code == 200:
                response.success()
            elif response.status_code in [429, 500, 502, 503, 504]:
                response.failure(f"Server error: {response.status_code}")
            else:
                response.failure(f"Unexpected status: {response.status_code}")

        except Exception as e:
            response_time = time.time() - start_time
            print(f"Request failed after {response_time:.2f}s: {e}")


class StepLoadShape(LoadTestShape):
    stages = [
        # More efficient progression - faster ramp up, shorter durations
        {"duration": 120, "users": 5, "spawn_rate": 2, "request_file": "ccs_5_destinations.json"},
        {"duration": 300, "users": 15, "spawn_rate": 5, "request_file": "ccs_5_destinations.json"},
        {"duration": 480, "users": 25, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},
        {"duration": 660, "users": 35, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},
        {"duration": 840, "users": 50, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},
        # Cool down period
        {"duration": 960, "users": 10, "spawn_rate": 10, "request_file": "ccs_5_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                # Only update file if it's different to avoid unnecessary I/O
                if current_file.get_file() != stage["request_file"]:
                    current_file.set_file(stage["request_file"])
                    print(f"Switching to file: {stage['request_file']} at {run_time}s")

                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None


# Add event listener for better monitoring
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"Load test starting with host: {environment.host}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print(f"Load test completed. Total requests: {environment.stats.total.num_requests}")
