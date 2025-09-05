import json
from locust import task, FastHttpUser, tag, between
import config as config


class SmallRequestUser(FastHttpUser):
    weight = 0  # Disabled for 3000 destination focus
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_3k')
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
    weight = 0  # Disabled for 3000 destination focus
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_3k')
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
    weight = 0  # Disabled for 3000 destination focus
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_3k')
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
    weight = 0  # Disabled for 3000 destination focus
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_3k')
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
    weight = 100  # Only active user class for 3000 destination testing
    wait_time = between(0.1, 0.5)
    host = config.BASE_HOST
    
    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.dumps(json.load(json_file))

    @tag('peak_3k')
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
