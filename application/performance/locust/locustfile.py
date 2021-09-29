import json
from locust import HttpUser, task, between, tag, TaskSet

wait_time = between(1, 2)

URL = 'https://aoap9pw296.execute-api.eu-west-2.amazonaws.com'


class FiveRequest(TaskSet):
    weight = 80

    host = URL

    def on_start(self):
        with open('application/mock/requests/ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('scen1')
    @task(100)
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class FiftyRequest(HttpUser):
    weight = 15
    host = 'https://aoap9pw296.execute-api.eu-west-2.amazonaws.com'

    def on_start(self):
        with open('application/mock/requests/ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class FiveHundredRequest(HttpUser):
    weight = 3
    host = 'https://aoap9pw296.execute-api.eu-west-2.amazonaws.com'

    def on_start(self):
        with open('application/mock/requests/ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class OneThousandFiveHundredRequest(HttpUser):
    weight = 1
    host = 'https://aoap9pw296.execute-api.eu-west-2.amazonaws.com'

    def on_start(self):
        with open('application/mock/requests/ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class ThreeThousandRequest(HttpUser):
    weight = 1
    host = 'https://aoap9pw296.execute-api.eu-west-2.amazonaws.com'

    def on_start(self):
        with open('application/mock/requests/ccs_3000_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)
