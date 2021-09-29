import json
from locust import HttpUser, task, between, tag
import build.docker

wait_time = between(1, 2)


class FiveRequest(HttpUser):
    weight = 80

    host = ' '

    def on_start(self):
        with open('/application/mock/requests/ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('tag1')
    @task(100)
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class FiftyRequest(HttpUser):
    weight = 15
    host = ''

    def on_start(self):
        with open('application/mock/requests/ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('tag2')
    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class FiveHundredRequest(HttpUser):
    weight = 3
    host = ''

    def on_start(self):
        with open('application/mock/requests/ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('tag3')
    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class OneThousandFiveHundredRequest(HttpUser):
    weight = 1
    host = ''

    def on_start(self):
        with open('application/mock/requests/ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('tag4')
    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)


class ThreeThousandRequest(HttpUser):
    weight = 1
    host = ''

    def on_start(self):
        with open('application/mock/requests/ccs_3000_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('tag5')
    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/core-dos-road-distance-test", data=self.payload, headers=headers)
