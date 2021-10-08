import json
from locust import task, FastHttpUser, tag, LoadTestShape, constant_pacing
import config as config


class FiveDest(FastHttpUser):
    weight = 80

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class FiftyDest(FastHttpUser):
    weight = 15

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class FiveHundredDest(FastHttpUser):
    weight = 3

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class OneThousandFiveHundredDest(FastHttpUser):
    weight = 1

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ThreeThousandDest(FastHttpUser):
    weight = 1

    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ColdStartFiveDest(FastHttpUser):
    weight = 80
    wait_time = constant_pacing(300)

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('coldStart', 'load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ColdStartFiftyDest(FastHttpUser):
    weight = 15
    wait_time = constant_pacing(300)

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('coldStart', 'load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ColdStartFiveHundredDest(FastHttpUser):
    weight = 3
    wait_time = constant_pacing(300)

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('coldStart', 'load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ColdStartOneThousandFiveHundredDest(FastHttpUser):
    weight = 1
    wait_time = constant_pacing(300)

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('coldStart', 'load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)


class ColdStartThreeThousandDest(FastHttpUser):
    weight = 1
    wait_time = constant_pacing(300)

    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.load(json_file)

    @tag('coldStart', 'load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)
