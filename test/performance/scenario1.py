import json
from locust import task, FastHttpUser, tag, between
import config as config


class SmallRequestUser(FastHttpUser):
    weight = 80
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))  # Pre-serialize

    @tag('peak_usage')
    @task
    def small_request(self):
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


class MediumRequestUser(FastHttpUser):
    weight = 15
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_usage')
    @task
    def medium_request(self):
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


class LargeRequestUser(FastHttpUser):
    weight = 3
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_usage')
    @task
    def large_request(self):
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


class ExtraLargeRequestUser(FastHttpUser):
    weight = 1
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_usage')
    @task
    def extra_large_request(self):
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


class MassiveRequestUser(FastHttpUser):
    weight = 1
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_usage')
    @task
    def massive_request(self):
        with self.client.post(
            config.API_ENDPOINT, 
            data=self.payload, 
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
